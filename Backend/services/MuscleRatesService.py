from collections import Counter
import dataclasses
from typing import Sequence
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

    def _apply_muscle_coefs_to_base_coefs(
        self, base_coefs: Counter, new_coefs: Sequence[dict[str, float]]
    ) -> Counter:
        return sum(
            (Counter(muscle_data) for muscle_data in new_coefs), start=base_coefs
        )

    async def _calculate_muscle_coef(self, workout_id) -> Counter:
        base_muscles_coef = await self._get_dict_muscle_list()

        trained_muscles_coef = (
            await self.uow.musclerepository.get_all_trained_muscles_from_workout(
                workout_id
            )
        )

        return self._apply_muscle_coefs_to_base_coefs(
            base_coefs=base_muscles_coef, new_coefs=trained_muscles_coef
        )

    async def get_muscle_distribution_list(
        self, user_id: UUID, workout_id: int
    ) -> dict:
        async with self.uow:
            all_muscles_with_coef = await self._calculate_muscle_coef(workout_id)

            result = {
                muscle: self.get_muscle_status(score)
                for muscle, score in all_muscles_with_coef.items()
            }

            return result
