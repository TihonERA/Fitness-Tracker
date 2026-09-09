from collections import Counter
import dataclasses
from uuid import UUID

from sqlalchemy import values

from Backend.utils.uow import UnitOfWork
from Backend.services.BaseService import BaseService


class MuscleRatesService(BaseService):
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    @staticmethod
    def get_muscle_status(score: int) -> str:
        if score < 1:
            return "undertrained"
        elif score > 2:
            return "overtrained"
        else:
            return "normalized"

    async def _get_dict_muscle_list(self) -> Counter:
        muscles_list = await self.uow.musclerepository.get_all_muscles()
        return Counter(dict.fromkeys(muscles_list, 0))

    async def get_muscle_distribution_list(
        self, user_id: UUID, workout_id: int
    ) -> dict:
        async with self.uow:
            all_muscles_with_coef = await self._get_dict_muscle_list()

            all_trained_muscles_in_workout = (
                await self.uow.musclerepository.get_all_trained_muscles_from_workout(
                    workout_id
                )
            )
            for muscle_data in all_trained_muscles_in_workout:
                all_muscles_with_coef.update(muscle_data)

            result = {
                name: self.get_muscle_status(score)
                for name, score in all_muscles_with_coef.items()
            }

            return result
