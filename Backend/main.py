from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .tasks.muscle_rates import cel_app
from Backend.schemas.base import TaskResponse
from .api.v1 import workout
from .core.config import settings
from celery.result import AsyncResult

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(workout.router)

@app.get(
    "/tasks/{task_id}",
    response_model=TaskResponse
)
async def get_task_result(task_id: str):
    task_result = AsyncResult(task_id, app=cel_app)

    result_data = None
    if task_result.ready():
        if task_result.status == "SUCCESS":
            result_data = task_result.result
        elif task_result.status == "FAILURE":
            result_data = str(task_result.result) 

    return TaskResponse(
        task_id=task_id,
        status=task_result.status,
        result=result_data
    )
