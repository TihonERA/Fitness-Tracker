import pytest
from httpx import AsyncClient, ASGITransport
from Backend.main import app
import sys
import asyncio

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