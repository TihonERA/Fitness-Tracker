from Backend.models.workout import Workout
from Backend.schemas.workout import (
    WorkoutCreate,
    WorkoutCreateDTO,
    WorkoutGetAllFilter,
    WorkoutGetAllFilterDTO,
    WorkoutUpdate,
)
from Backend.services.base_service_components.delete_components import (
    DeleteAuthorizedService,
)
from Backend.services.base_service_components.interfaces import (
    DeleteAuthorizedServiceInterface,
    ReadAllServiceInterface,
    ReadRelationAuthorizedServiceInterface,
    RegisterServiceInterface,
    UpdateAuthorizedServiceInterface,
)

from Backend.services.base_service_components.create_components import RegisterService
from Backend.services.base_service_components.read_all_component import (
    ReadAllAuthorizedService,
)
from Backend.services.base_service_components.read_components.mixins import (
    ReadRelationAuthorizedService,
)
from Backend.infrastructure.WorkoutRepository import WorkoutRepository
from Backend.services.base_service_components.update_components import (
    UpdateAuthorizedService,
)
from Backend.services.workout.interfaces import (
    WorkoutDeleteAuthServiceInterface,
    WorkoutReadAllServiceInterface,
    WorkoutReadRelationAuthServiceInterface,
    WorkoutRegisterServiceInterface,
    WorkoutUpdateAuthServiceInterface,
)


class WorkoutRegisterService(
    RegisterService[Workout, WorkoutRepository, WorkoutCreate, WorkoutCreateDTO],
    WorkoutRegisterServiceInterface,
):
    pass


class WorkoutReadRelationAuthService(
    ReadRelationAuthorizedService[Workout, WorkoutRepository],
    WorkoutReadRelationAuthServiceInterface,
):
    pass


class WorkoutReadAllService(
    ReadAllAuthorizedService[
        Workout, WorkoutRepository, WorkoutGetAllFilter, WorkoutGetAllFilterDTO
    ],
    WorkoutReadAllServiceInterface,
):
    pass


class WorkoutUpdateAuthService(
    UpdateAuthorizedService[Workout, WorkoutRepository, WorkoutUpdate],
    WorkoutUpdateAuthServiceInterface,
):
    pass


class WorkoutDeleteAuthService(
    DeleteAuthorizedService[Workout, WorkoutRepository],
    WorkoutDeleteAuthServiceInterface,
):
    pass
