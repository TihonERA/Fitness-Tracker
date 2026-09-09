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

    async def _get_dict_muscle_list(self) -> dict[str, int]:
        muscles_list = await self.uow.musclerepository.get_all_muscles()
        return dict.fromkeys(muscles_list, 0)

    async def get_muscle_distribution_list(
        self, user_id: UUID, workout_id: int
    ) -> dict:
        async with self.uow:
            all_muscles = await self._get_dict_muscle_list()

            all_trained_muscles_unfiltered = [
                items
                for data in await self.uow.musclerepository.get_all_trained_muscles_from_workout(
                    workout_id
                )
                for items in data.items()
            ]

            all_muscles = {
                name: all_muscles[name] + score
                for name, score in all_trained_muscles_unfiltered
            }

            result = {
                name: self.get_muscle_status(score)
                for name, score in all_muscles.items()
            }

            return result
