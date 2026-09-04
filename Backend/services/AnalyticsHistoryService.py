from typing import Any, overload, override
from uuid import UUID

from alembic.command import current

from Backend.models.sets_history import SetsHistory
from Backend.services.TrainingDayHistoryService import TrainingDayHistoryService
from Backend.utils.exceptions import NotFound
from Backend.utils.uow import UnitOfWork

from Backend.schemas.AnalyticsHistory import (
    CreateHistory,
    ExerciseDifference,
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

        last_training_exercise_id_set = set()

        if last_training is not None:
            for ex in last_training.exercises_history:
                last_training_exercise_id_set.add(ex.exercise_id)

        last_tr_index = 0
        new_tr_index = 0

        differences: list[ExerciseDifference] = []
        while (new_tr_index < len(data.exercises)) and last_training:
            last = last_training.exercises_history[last_tr_index]

            exercise_data = ExerciseHistoryCreateDTO(
                user_id=user_id,
                training_day_history_id=new_training.id,
                **data.exercises[new_tr_index].model_dump(exclude_unset=True),
            )
            new = await self.ex_history_service.create_exercise_history(exercise_data)

            difference = ExerciseDifference(exercise_id=new.exercise_id)

            if last.exercise_id != new.exercise_id:
                difference.exercise_id = None
                differences.append(difference)
                new_tr_index += 1
                continue

            difference.sets_differences = self.get_sets_differences(
                last.sets_history, new.sets_history
            )

            differences.append(difference)

            new_tr_index += 1
            last_tr_index += 1

        last_training = (
            TrainingDayHistoryResponse.model_validate(last_training)
            if last_training is not None
            else None
        )
        loaded_new_training = (
            await self.tr_day_history_service.get_loaded_tr_day_history(new_training.id)
        )
        loaded_new_training = TrainingDayHistoryResponse.model_validate(
            loaded_new_training
        )
        response = HistoryResponse(
            last_training=last_training,
            new_training=loaded_new_training,
            differences=differences,
        )

        return response

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
