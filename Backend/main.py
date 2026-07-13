from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from .tasks.muscle_rates import cel_app
from Backend.schemas.base import TaskResponse
from .api.v1 import workout
from .core.config import settings
from celery.result import AsyncResult
from celery import states
from .utils.validators import NotFound
import asyncio

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

    if task_result.state in states.UNREADY_STATES:
        return TaskResponse(
            task_id=task_id,
            status=task_result.status,
            result=None
        )

    try:
        result = await asyncio.to_thread(
            task_result.get,
            timeout=0.1,
            propagate=True
        )

        return TaskResponse(
            task_id=task_id,
            status=states.SUCCESS,
            result=result
        )
    except NotFound as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
