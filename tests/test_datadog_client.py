from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock

from asyncstatsd.client import DatadogClient

from .testing import EventLoopMockMixin, RandomMockMixin, TimenowMockMixin


class TestDatadogClient(IsolatedAsyncioTestCase, EventLoopMockMixin, RandomMockMixin, TimenowMockMixin):
    def setUp(self):
        self._create_loop_mock()
        self.loop_mock.create_datagram_endpoint.return_value = MagicMock(), MagicMock()

    async def asyncSetUp(self):
        self.client = DatadogClient("localhost", 8125)
        self.addCleanup(self.client.close)
        await self.client.connect()
        self.addAsyncCleanup(self.client.close)

    def test_increment(self):
        self.client.incr("test", tags=dict(test_tag="test"))
        self.client._transport.sendto.assert_called_once_with(b"test:1|c|#test_tag:test")

    def test_decrement(self):
        self.client.decr("test", tags=dict(test_tag="test"))
        self.client._transport.sendto.assert_called_once_with(b"test:-1|c|#test_tag:test")

    def test_gauge(self):
        self.client.gauge("test", 30, tags=dict(test_tag="test"))
        self.client._transport.sendto.assert_called_once_with(b"test:30|g|#test_tag:test")

    def test_gauge_delta(self):
        self.client.gauge("test", 30, delta=True, tags=dict(test_tag="test"))
        self.client._transport.sendto.assert_called_once_with(b"test:+30|g|#test_tag:test")

    def test_gauge_rate(self):
        self.client.gauge("test", 30, 1.0, tags=dict(test_tag="test"))
        self.client._transport.sendto.assert_called_once_with(b"test:30|g|#test_tag:test")

    def test_gauge_rate_delta(self):
        self.client.gauge("test", 30, 1.0, delta=True, tags=dict(test_tag="test"))
        self.client._transport.sendto.assert_called_once_with(b"test:+30|g|#test_tag:test")

    def test_set(self):
        self.client.set("test", 30, tags=dict(test_tag="test"))
        self.client._transport.sendto.assert_called_once_with(b"test:30|s|#test_tag:test")

    def test_timing(self):
        self.client.timing("test", 100, tags=dict(test_tag="test"))
        self.client._transport.sendto.assert_called_once_with(b"test:100.000000|ms|#test_tag:test")
