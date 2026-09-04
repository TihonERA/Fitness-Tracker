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
    def __init__(self, uow: UnitOfWork) -> None:
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
                new = await uow.exercisehistory.create_exercise_history(exercise_data)

                differences.append(ExerciseDifference(exercise_id=new.exercise_id))
                current_difference = differences[new_tr_index]

                if last.exercise_id != new.exercise_id:
                    current_difference.exercise_id = None
                    new_tr_index += 1
                    continue

                last_sets_length = len(last.sets_history)
                new_sets_length = len(new.sets_history)

                for i in range(max(last_sets_length, new_sets_length)):
                    current_difference.sets_differences.append(SetsDifference())

                    if i >= last_sets_length or i >= new_sets_length:
                        continue

                    old_current_set = last.sets_history[i]
                    new_current_set = new.sets_history[i]

                    if new_current_set.reps is None or old_current_set.reps is None:
                        continue

                    current_difference.sets_differences[i].reps = (
                        self.calc_diff_return_none_if_zero(
                            first=new_current_set.reps,
                            second=old_current_set.reps,
                        )
                    )
                    if new_current_set.weight is None or old_current_set.weight is None:
                        continue

                    current_difference.sets_differences[i].weight = (
                        self.calc_diff_return_none_if_zero(
                            first=new_current_set.weight,
                            second=old_current_set.weight,
                        )
                    )
                new_tr_index += 1
                last_tr_index += 1

            last_training = (
                TrainingDayHistoryResponse.model_validate(last_training)
                if last_training is not None
                else None
            )
            loaded_new_training = await uow.trainingdayhistory.get_tr_day_history(
                new_training.id
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
