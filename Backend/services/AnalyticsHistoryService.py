from typing import Any, overload, override
from uuid import UUID

from alembic.command import current

from Backend.services.TrainingDayHistoryService import TrainingDayHistoryService
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
        uow: UnitOfWork,
        ex_hist_service: ExerciseHistoryService,
        tr_day_hist_service: TrainingDayHistoryService,
    ) -> None:
        self.uow = uow

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
        async with self.uow as uow:
            tr_day_history_data = TrainingDayHistoryCreate(
                day_name=data.day_name, day_id=data.day_id
            )

            last_training = await uow.trainingdayhistory.get_last_history(user_id)
            new_training = await uow.trainingdayhistory.create_instance(
                tr_day_history_data
            )

            response = HistoryResponse(
                last_training=TrainingDayHistoryResponse.model_validate(last_training),
                new_training=TrainingDayHistoryResponse.model_validate(new_training),
            )

            last_tr_index = 0
            new_tr_index = 0

            while (new_tr_index < len(data.exercises)) and last_training:
                old = last_training.exercises_history[last_tr_index]

                exercise_data = ExerciseHistoryCreateDTO(
                    user_id=user_id,
                    **data.exercises[new_tr_index].model_dump(exclude_unset=True),
                )
                new = await uow.exercisehistory.create_exercise_history(exercise_data)
                response.differences.append(
                    ExerciseDifference(exercise_id=new.exercise_id)
                )
                current_difference = response.differences[new_tr_index]

                if old.exercise_id != new.exercise_id:
                    current_difference.exercise_id = None
                    new_tr_index += 1
                    continue

                old_sets_length = len(old.sets_history)
                new_sets_length = len(new.sets_history)

                for i in range(max(old_sets_length, new_sets_length)):
                    old_or_new_exercise_id = (
                        old.exercise_id if i < old_sets_length else new.exercise_id
                    )
                    set_number = i + 1
                    current_difference.sets_differences[set_number] = SetsDifference()

                    if i < old_sets_length and i < new_sets_length:
                        old_current_set = old.sets_history[i]
                        new_current_set = new.sets_history[i]

                        if new_current_set.reps and old_current_set.reps:
                            current_difference.sets_differences[set_number].reps = (
                                self.calc_diff_return_none_if_zero(
                                    first=new_current_set.reps,
                                    second=old_current_set.reps,
                                )
                            )
                        if new_current_set.weight and old_current_set.weight:
                            current_difference.sets_differences[set_number].weight = (
                                self.calc_diff_return_none_if_zero(
                                    first=new_current_set.weight,
                                    second=old_current_set.weight,
                                )
                            )
                new_tr_index += 1
                last_tr_index += 1

            return response
