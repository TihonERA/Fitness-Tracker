from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1 import workout
from .core.config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(workout.router)