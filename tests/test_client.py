import asyncio
from unittest import IsolatedAsyncioTestCase

from aiostatsd.client import StatsdClient, StatsdClientBase
from aiostatsd.metrics import CounterMetric

from .testing import EventLoopMockMixin, RandomMockMixin, TimenowMockMixin


class TestStatsdClientBase(IsolatedAsyncioTestCase, EventLoopMockMixin, RandomMockMixin):
    def setUp(self):
        self._create_loop_mock()
        self._create_random_mock("aiostatsd.client.random")

    async def asyncSetUp(self):
        self.client = StatsdClientBase("localhost", 8125)
        self.addCleanup(self.client.close)
        await self.client.connect()
        self.addAsyncCleanup(self.client.close)

    async def test_sending_when_rate_fits(self):
        counter = CounterMetric("test", rate=0.5)
        await self.client.send(counter)
        self.client._transport.sendto.assert_called_once_with(b"test:1|c|@0.5")

    async def test_sending_when_rate_does_not_fit(self):
        counter = CounterMetric("test", rate=0.4)
        await self.client.send(counter)
        self.client._transport.sendto.assert_not_called()


class TestStatsdClient(IsolatedAsyncioTestCase, EventLoopMockMixin, RandomMockMixin, TimenowMockMixin):
    def setUp(self):
        self._create_loop_mock()
        self._create_random_mock("aiostatsd.client.random")
        self._create_timenow_mock("aiostatsd.client.time_now")

    async def asyncSetUp(self):
        self.client = StatsdClient("localhost", 8125)
        self.addCleanup(self.client.close)
        await self.client.connect()
        self.addAsyncCleanup(self.client.close)

    async def test_increment(self):
        await self.client.incr("test")
        self.client._transport.sendto.assert_called_once_with(b"test:1|c")

    async def test_decrement(self):
        await self.client.decr("test")
        self.client._transport.sendto.assert_called_once_with(b"test:-1|c")

    async def test_gauge(self):
        await self.client.gauge("test", 30)
        self.client._transport.sendto.assert_called_once_with(b"test:30|g")

    async def test_set(self):
        await self.client.set("test", 30)
        self.client._transport.sendto.assert_called_once_with(b"test:30|s")

    async def test_timing(self):
        await self.client.timing("test", 100)
        self.client._transport.sendto.assert_called_once_with(b"test:100.000000|ms")

    async def test_timing_with_rate(self):
        self.timenow_mock.side_effect = [0.1, 0.2]
        async with self.client.timer("test", rate=0.5):
            await asyncio.sleep(0.1)
        self.client._transport.sendto.assert_called_once_with(b"test:100.000000|ms|@0.5")
