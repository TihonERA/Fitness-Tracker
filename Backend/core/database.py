from .config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from redis.asyncio import Redis

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=False
)

async_session_factory = async_sessionmaker(
    async_engine,
    expire_on_commit=False
)
