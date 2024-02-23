from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock

from asyncstatsd.client.udp import UDPClient

from .testing import EventLoopMockMixin


class TestUDPConnection(IsolatedAsyncioTestCase, EventLoopMockMixin):
    def setUp(self):
        self._create_loop_mock()
        self.loop_mock.create_datagram_endpoint.return_value = MagicMock(), MagicMock()
        self.udp_conn = UDPClient("localhost", 8125)
        self.addCleanup(self.udp_conn.close)

    async def test_connect(self):
        await self.udp_conn.connect()


class TestUDPConnectionErrorHandling(IsolatedAsyncioTestCase):
    def setUp(self):
        self.udp_conn = UDPClient("localhost", 8125)

    async def test_cleanup_on_connection_lost(self):
        await self.udp_conn.connect()
        self.udp_conn._transport.close()
        await self.udp_conn._on_con_lost
