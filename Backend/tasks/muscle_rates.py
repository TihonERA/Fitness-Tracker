# Backend/tasks/muscle_rates.py
import asyncio
import logging
from celery import Celery
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from ..services.WorkoutService import WorkoutService
from ..core.database import get_redis
from ..core import celeryconfig
from ..core.config import settings

logger = logging.getLogger(__name__)

cel_app = Celery("workout_rate")
cel_app.config_from_object(celeryconfig)

def get_isolated_sessionmaker():
    engine = create_async_engine(
        settings.DATABASE_URL_asyncpg, 
        poolclass=NullPool
    )
    return async_sessionmaker(bind=engine, expire_on_commit=False)

@cel_app.task
def get_muscles_balance(workout_id: int):
    
    try:
        async def _run():
            sessionmaker = get_isolated_sessionmaker()
            async with sessionmaker() as session:
                redis = get_redis()
                service = WorkoutService(session=session, redis=redis)
                
                result = await service.get_muscles_balance(workout_id=workout_id)
                return result
        
        return asyncio.run(_run())
        
    except Exception as e:
        logger.error(f"=== ОШИБКА В ЗАДАЧЕ: {e} ===")
        logger.error(f"=== ТИП ОШИБКИ: {type(e)} ===")
        logger.error(f"=== TRACEBACK ===", exc_info=True)
        raise

@cel_app.task
def get_muscle_contribution_list(workout_id: int):
    try:
        async def _run():
            sessionmaker = get_isolated_sessionmaker()
            async with sessionmaker() as session:
                redis = get_redis()
                service = WorkoutService(session=session, redis=redis)
                return await service.get_muscles_distribution_list(workout_id=workout_id)
        
        return asyncio.run(_run())
    except Exception as e:
        logger.error(f"=== ОШИБКА В ЗАДАЧЕ: {e} ===")
        logger.error(f"=== ТИП ОШИБКИ: {type(e)} ===")
        logger.error(f"=== TRACEBACK ===", exc_info=True)
        raise
