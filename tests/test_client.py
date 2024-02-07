from unittest import IsolatedAsyncioTestCase

from aiostatsd.client import StatsdClient, StatsdClientBase
from aiostatsd.metrics.basic import CounterMetric

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

    def test_sending_when_rate_fits(self):
        counter = CounterMetric("test", rate=0.5)
        self.client.send(counter)
        self.client._transport.sendto.assert_called_once_with(b"test:1|c|@0.5")

    def test_sending_when_rate_does_not_fit(self):
        counter = CounterMetric("test", rate=0.4)
        self.client.send(counter)
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

    def test_increment(self):
        self.client.incr("test")
        self.client._transport.sendto.assert_called_once_with(b"test:1|c")

    def test_decrement(self):
        self.client.decr("test")
        self.client._transport.sendto.assert_called_once_with(b"test:-1|c")

    def test_gauge(self):
        self.client.gauge("test", 30)
        self.client._transport.sendto.assert_called_once_with(b"test:30|g")

    def test_set(self):
        self.client.set("test", 30)
        self.client._transport.sendto.assert_called_once_with(b"test:30|s")

    def test_timing(self):
        self.client.timing("test", 100)
        self.client._transport.sendto.assert_called_once_with(b"test:100.000000|ms")

    def test_timing_with_rate(self):
        self.timenow_mock.side_effect = [0.1, 0.2]
        with self.client.timer("test", rate=0.5):
            pass
        self.client._transport.sendto.assert_called_once_with(b"test:100.000000|ms|@0.5")
