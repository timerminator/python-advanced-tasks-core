import pytest
from aresponses import ResponsesMockServer


# fix for aiohttp_client + aresponses
# https://github.com/aresponses/aresponses#:~:text=If%20you%27re%20trying%20to%20use%20the%20aiohttp_client%20test%20fixture
@pytest.fixture
def loop(event_loop):
    """replace aiohttp loop fixture with pytest-asyncio fixture"""
    return event_loop


# working with pytest-aiohttp
# If you need to use aresponses together with pytest-aiohttp, you should re-initialize the main aresponses fixture with the loop fixture
# https://github.com/aresponses/aresponses#:~:text=If%20you%20need%20to%20use%20aresponses%20together%20with%20pytest%2Daiohttp
@pytest.fixture
async def aresponses(loop) -> ResponsesMockServer:
    async with ResponsesMockServer(loop=loop) as server:
        yield server
