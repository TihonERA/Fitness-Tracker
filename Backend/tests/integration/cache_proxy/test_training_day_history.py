from typing import Callable

import pytest
from redis.asyncio import Redis

from Backend.models import training_day_history
from Backend.schemas.training_day_history import (
    TrainingDayHistoryCreate,
    TrainingDayHistoryGetAll,
)
from Backend.utils.uow import UnitOfWork

from Backend.tests.integration.conftest import TrDayDatas, TrDayData

from Backend.schemas.training_day_history import TrainingDayHistoryCachePrefixes

from Backend.cache_proxies.key_formatters.TrainingDayHistoryCacheKeyFormatter import (
    TrainingDayHistoryCacheKeyFormatter,
)
from Backend.cache_proxies.invalidators.TrainingDayHistoryCacheInvalidator import (
    TrainingDayHistoryCacheInvalidator,
)
from Backend.cache_proxies.TrainingDayHistoryCacheProxy import (
    TrainingDayHistoryCacheProxy,
)

from Backend.services.TrainingDayHistoryService import TrainingDayHistoryService
from Backend.tests.integration.cache_proxy.conftest import keys_func


@pytest.mark.asyncio(loop_scope="session")
class TestTrainingDayHistoryCacheProxy:

    @pytest.fixture
    def proxy(self, uow: UnitOfWork, redis: Redis):
        formatter = TrainingDayHistoryCacheKeyFormatter()
        invalidator = TrainingDayHistoryCacheInvalidator(redis, formatter)
        service = TrainingDayHistoryService(uow)
        return TrainingDayHistoryCacheProxy(service, redis, invalidator, formatter)

    @pytest.fixture
    def get_training_day_history_version_key(self, redis: Redis):
        async def _func():
            match = TrainingDayHistoryCachePrefixes.version + ":*"

            return [key async for key in redis.scan_iter(match=match)]

        return _func

    @pytest.fixture
    def get_all_training_day_history_key(self, redis: Redis):
        async def _func():
            match = TrainingDayHistoryCachePrefixes.get_all_key + ":*"

            return [key async for key in redis.scan_iter(match=match)]

        return _func

    @pytest.fixture
    def get_tag_training_day_history_key(self, redis: Redis):
        async def _func():
            match = TrainingDayHistoryCachePrefixes.tag + ":*"

            return [key async for key in redis.scan_iter(match=match)]

        return _func

    @pytest.fixture
    def get_loaded_training_day_history_key(self, redis: Redis):
        async def _func():
            match = TrainingDayHistoryCachePrefixes.get_loaded_key + ":*"

            return [key async for key in redis.scan_iter(match=match)]

        return _func

    async def test_get_all(
        self,
        proxy: TrainingDayHistoryCacheProxy,
        tr_history_datas: TrDayDatas,
        get_all_training_day_history_key: keys_func,
    ):
        data = TrainingDayHistoryGetAll(skip=0, limit=50)

        await proxy.get_all_tr_day_history(user_id=tr_history_datas.user_id, data=data)

        assert len(await get_all_training_day_history_key()) > 0

    async def test_get_loaded(
        self,
        proxy: TrainingDayHistoryCacheProxy,
        tr_history_data: TrDayData,
        get_tag_training_day_history_key: keys_func,
        get_loaded_training_day_history_key: keys_func,
    ):
        await proxy.get_loaded_tr_day_history(
            user_id=tr_history_data.user_id, history_id=tr_history_data.history.id
        )

        assert len(await get_tag_training_day_history_key()) > 0
        assert len(await get_loaded_training_day_history_key()) > 0

    async def test_create(
        self,
        proxy: TrainingDayHistoryCacheProxy,
        tr_history_datas: TrDayDatas,
        get_training_day_history_version_key: keys_func,
    ):
        await proxy.get_all_tr_day_history(
            user_id=tr_history_datas.user_id,
            data=TrainingDayHistoryGetAll(skip=0, limit=50),
        )

        data = TrainingDayHistoryCreate(
            day_name="name", day_id=tr_history_datas.histories[0].day_id
        )

        await proxy.create_history(user_id=tr_history_datas.user_id, data=data)

        assert (len(await get_training_day_history_version_key())) > 0

    async def test_delete(
        self,
        proxy: TrainingDayHistoryCacheProxy,
        tr_history_datas: TrDayDatas,
        get_loaded_training_day_history_key: keys_func,
        get_training_day_history_version_key: keys_func,
    ):
        user_id = tr_history_datas.user_id
        id = tr_history_datas.histories[0].id

        await proxy.get_loaded_tr_day_history(user_id=user_id, history_id=id)
        await proxy.get_all_tr_day_history(
            user_id=user_id, data=TrainingDayHistoryGetAll(skip=0, limit=50)
        )

        assert len(await get_loaded_training_day_history_key()) > 0
        assert len(await get_training_day_history_version_key()) == 0

        await proxy.delete_history(user_id=user_id, history_id=id)

        assert len(await get_loaded_training_day_history_key()) == 0
        assert len(await get_training_day_history_version_key()) > 0
