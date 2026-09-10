from collections import Counter
import dataclasses
from typing import Final, Sequence
from uuid import UUID

from sqlalchemy import values

from Backend.utils.uow import UnitOfWork
from Backend.services.BaseService import BaseService


class MuscleRatesService(BaseService):
    ZERO_RATIO: Final = 0
    LOWEST_RATIO_BORDER: Final = 0.5
    HIGHEST_RATIO_BORDER: Final = 1.5

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

    async def get_muscle_distribution_list(self, workout_id: int) -> dict[str, str]:
        async with self.uow:
            all_muscles_with_coef = await self._calculate_muscle_coef(workout_id)

            result = {
                muscle: self.get_muscle_status(score)
                for muscle, score in all_muscles_with_coef.items()
            }

            return result

    def get_ratio_between_coef(self, first_coef: float, second_coef: float) -> float:
        if second_coef == 0:
            return self.ZERO_RATIO
        return first_coef / second_coef

    def is_ratio_between_borders(self, ratio: float) -> bool:
        return self.LOWEST_RATIO_BORDER < ratio < self.HIGHEST_RATIO_BORDER

    def get_ratio_message(
        self, first_muscle: str, second_muscle: str, ratio: float
    ) -> str:
        if self.is_ratio_between_borders(ratio):
            return f"{second_muscle} is balanced in comparison to {first_muscle}"

        if ratio > self.HIGHEST_RATIO_BORDER:
            return f"{second_muscle} is undertrained in comparison to {first_muscle}"

        return f"{second_muscle} is overtrained in comparison to {first_muscle}"

    def make_muscle_antagonist_balance_info(
        self,
        muscle: str,
        muscle_coef: float,
        muscle_antagonist: str,
        muscle_antagonist_coef: float,
    ) -> dict[str, str | bool]:
        ratio = self.get_ratio_between_coef(muscle_coef, muscle_antagonist_coef)

        return {
            "muscle": muscle,
            "muscle_antagonist": muscle_antagonist,
            "balanced": self.is_ratio_between_borders(ratio),
            "message": self.get_ratio_message(
                first_muscle=muscle, second_muscle=muscle_antagonist, ratio=ratio
            ),
        }

    async def get_muscle_antagonists_statuses(
        self, workout_id: int
    ) -> list[dict[str, str | bool]]:
        async with self.uow:
            all_muscle_antagonists = {
                muscle: muscle_antagonist
                for muscle, muscle_antagonist in await self.uow.musclerepository.get_all_muscles_antagonists()
            }

            all_muscles_with_coef = await self._calculate_muscle_coef(workout_id)

            result = [
                self.make_muscle_antagonist_balance_info(
                    muscle=muscle,
                    muscle_coef=all_muscles_with_coef[muscle],
                    muscle_antagonist=muscle_antagonist,
                    muscle_antagonist_coef=all_muscles_with_coef[muscle_antagonist],
                )
                for muscle, muscle_antagonist in all_muscle_antagonists.items()
            ]

            return result
