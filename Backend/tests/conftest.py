import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.engine import create
from Backend.main import app
import sys
import asyncio
from ..models.base import Base
from ..core.database import async_engine 

@pytest.fixture(scope="session")
def event_loop():
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()

@pytest.fixture(scope="function")
async def client(event_loop):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c

@pytest.fixture(autouse=True)
async def setup_and_teardown_database():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    yield
