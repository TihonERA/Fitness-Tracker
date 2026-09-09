from uuid import UUID

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

    async def get_muscle_distribution_list(
        self, user_id: UUID, workout_id: int
    ) -> dict:
        async with self.uow as uow:
            all_muscles = {muscle: 0 for muscle in await uow.musclerepository.get_all()}

            all_trained_muscles_unfiltered = (
                await uow.musclerepository.get_all_trained_muscles_from_workout(
                    workout_id
                )
            )

            for name, score in all_trained_muscles_unfiltered:
                if name in all_muscles:
                    all_muscles[name] += score
                else:
                    all_muscles[name] = score

            result = {
                name: self.get_muscle_status(score)
                for name, score in all_muscles.items()
            }

            return result
