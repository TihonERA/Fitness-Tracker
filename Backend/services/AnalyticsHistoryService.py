from typing import Any, overload, override
from uuid import UUID

import asyncio

from alembic.command import current

from Backend.models.exercise_history import ExerciseHistory
from Backend.models.sets_history import SetsHistory
from Backend.models.training_day_history import TrainingDayHistory
from Backend.services.TrainingDayHistoryService import TrainingDayHistoryService
from Backend.utils.exceptions import NotFound
from Backend.utils.uow import UnitOfWork

from Backend.schemas.AnalyticsHistory import (
    CreateHistory,
    ExerciseDifference,
    ExerciseHistoryCreateNested,
    HistoryResponse,
    SetsDifference,
)
from Backend.schemas.exercise_history import ExerciseHistoryCreateDTO
from Backend.schemas.training_day_history import (
    TrainingDayHistoryCreate,
    TrainingDayHistoryResponse,
)
from Backend.services.ExerciseHistoryService import ExerciseHistoryService


class AnalyticsHistoryService:
    def __init__(
        self,
        tr_day_history_service: TrainingDayHistoryService,
        ex_history_service: ExerciseHistoryService,
    ) -> None:
        self.tr_day_history_service = tr_day_history_service
        self.ex_history_service = ex_history_service

    @overload
    def calc_diff_return_none_if_zero(self, first: int, second: int) -> int | None: ...

    @overload
    def calc_diff_return_none_if_zero(
        self, first: float, second: float
    ) -> float | None: ...

    def calc_diff_return_none_if_zero(
        self, first: int | float, second: int | float
    ) -> int | float | None:
        difference = first - second
        if difference <= 0:
            return None
        return difference

    async def get_last_history_or_none(
        self, user_id: UUID
    ) -> TrainingDayHistory | None:
        try:
            return await self.tr_day_history_service.get_last_history(user_id)
        except NotFound:
            return None

    async def create_history(
        self, user_id: UUID, data: CreateHistory
    ) -> HistoryResponse:
        tr_day_history_data = TrainingDayHistoryCreate(
            day_name=data.day_name, day_id=data.day_id
        )

        last_tr_day_history = await self.get_last_history_or_none(user_id)
        new_tr_day_history = await self.tr_day_history_service.create_history(
            tr_day_history_data
        )

        if last_tr_day_history is None:
            for new_ex_creation_data in data.exercises:
                await self.create_new_history(
                    user_id=user_id,
                    training_day_history_id=new_tr_day_history.id,
                    data=new_ex_creation_data,
                )

            response = await self.make_history_response_and_load_new_training(
                new_tr_day_history=new_tr_day_history
            )

            return response

        last_training_exercise_id_set = {
            ex.exercise_id for ex in last_tr_day_history.exercises_history
        }

        differences = await asyncio.gather(
            *[
                self.get_exercise_difference(
                    user_id=user_id,
                    training_day_history_id=new_tr_day_history.id,
                    last_ex_history=last_ex_history,
                    new_ex_creation_data=new_ex_creation_data,
                    last_training_exercise_id_set=last_training_exercise_id_set,
                )
                for last_ex_history, new_ex_creation_data in zip(
                    last_tr_day_history.exercises_history, data.exercises
                )
            ]
        )

        response = await self.make_history_response_and_load_new_training(
            new_tr_day_history=new_tr_day_history,
            last_tr_day_history=last_tr_day_history,
            differences=differences,
        )
        return response

    async def make_history_response_and_load_new_training(
        self,
        new_tr_day_history: TrainingDayHistory,
        last_tr_day_history: TrainingDayHistory | None = None,
        differences: list[ExerciseDifference] = [],
    ) -> HistoryResponse:
        new_tr_day_history = (
            await self.tr_day_history_service.get_loaded_tr_day_history(
                new_tr_day_history.id
            )
        )
        return HistoryResponse.model_validate(
            {
                "last_training": last_tr_day_history,
                "new_training": new_tr_day_history,
                "differences": differences,
            }
        )

    async def create_new_history(
        self,
        user_id: UUID,
        training_day_history_id: int,
        data: ExerciseHistoryCreateNested,
    ) -> ExerciseHistory:
        exercise_data = ExerciseHistoryCreateDTO(
            user_id=user_id,
            training_day_history_id=training_day_history_id,
            **data.model_dump(exclude_unset=True),
        )
        new = await self.ex_history_service.create_exercise_history(exercise_data)

        return new

    async def get_exercise_difference(
        self,
        user_id: UUID,
        training_day_history_id: int,
        last_ex_history: ExerciseHistory,
        new_ex_creation_data: ExerciseHistoryCreateNested,
        last_training_exercise_id_set: set[int],
    ) -> ExerciseDifference:
        new_ex_history = await self.create_new_history(
            user_id=user_id,
            training_day_history_id=training_day_history_id,
            data=new_ex_creation_data,
        )

        difference = ExerciseDifference()

        if new_ex_history.exercise_id not in last_training_exercise_id_set:
            return difference

        difference.exercise_id = new_ex_history.exercise_id
        difference.sets_differences = self.get_sets_differences(
            last_ex_history.sets_history, new_ex_history.sets_history
        )

        return difference

    def compare_sets(
        self, first_set: SetsHistory, second_set: SetsHistory
    ) -> SetsDifference:
        set_difference = SetsDifference()

        if first_set.reps and second_set.reps:
            set_difference.reps = self.calc_diff_return_none_if_zero(
                first_set.reps, second_set.reps
            )

        if first_set.weight and second_set.weight:
            set_difference.weight = self.calc_diff_return_none_if_zero(
                first_set.weight, second_set.weight
            )

        return set_difference

    def get_sets_differences(
        self,
        first_sets_history: list[SetsHistory],
        second_sets_history: list[SetsHistory],
    ) -> list[SetsDifference]:
        differences = [
            self.compare_sets(first_set, second_set)
            for first_set, second_set in zip(first_sets_history, second_sets_history)
        ]

        return differences
