from typing import Any, overload, override
from uuid import UUID

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

    async def create_history(
        self, user_id: UUID, data: CreateHistory
    ) -> HistoryResponse:
        tr_day_history_data = TrainingDayHistoryCreate(
            day_name=data.day_name, day_id=data.day_id
        )

        try:
            last_training = await self.tr_day_history_service.get_last_history(user_id)
        except NotFound:
            last_training = None

        new_training = await self.tr_day_history_service.create_history(
            tr_day_history_data
        )

        if last_training is None:
            for new_ex_creation_data in data.exercises:
                await self.create_new_history(
                    user_id=user_id,
                    training_day_history_id=new_training.id,
                    data=new_ex_creation_data,
                )

            loaded_new_training = await self.load_relations_in_new_training(
                new_training
            )

            return self.make_history_response(new_training=loaded_new_training)
        last_training_exercise_id_set = {
            ex.exercise_id for ex in last_training.exercises_history
        }

        differences = [
            await self.get_exercise_difference(
                user_id=user_id,
                training_day_history_id=new_training.id,
                last_ex_history=last_ex_history,
                new_ex_creation_data=new_ex_creation_data,
            )
            for last_ex_history, new_ex_creation_data in zip(
                last_training.exercises_history, data.exercises
            )
        ]

        loaded_new_training = await self.load_relations_in_new_training(new_training)
        response = self.make_history_response(
            new_training=loaded_new_training,
            last_training=last_training,
            differences=differences,
        )
        return response

    def make_history_response(
        self,
        new_training: TrainingDayHistory,
        last_training: TrainingDayHistory | None = None,
        differences: list[ExerciseDifference] = [],
    ) -> HistoryResponse:
        return HistoryResponse.model_validate(
            {
                "last_training": last_training,
                "new_training": new_training,
                "differences": differences,
            }
        )

    async def load_relations_in_new_training(
        self, new_training: TrainingDayHistory
    ) -> TrainingDayHistory:
        loaded = await self.tr_day_history_service.get_loaded_tr_day_history(
            new_training.id
        )
        return loaded

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
    ) -> ExerciseDifference:
        new_ex_history = await self.create_new_history(
            user_id=user_id,
            training_day_history_id=training_day_history_id,
            data=new_ex_creation_data,
        )

        difference = ExerciseDifference()

        if last_ex_history.exercise_id != new_ex_history.exercise_id:
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
