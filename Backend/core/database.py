from .config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from redis import Redis

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True
)

async_session_factory = async_sessionmaker(
    async_engine,
    expire_on_commit=False
)

async def get_db():
    async with async_session_factory() as session:
        yield session

def get_redis():
    return Redis(settings.REDIS_HOST, settings.REDIS_PORT, decode_responses=True)