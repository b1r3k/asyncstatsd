from unittest import IsolatedAsyncioTestCase

from aiostatsd.udp import UDPClient

from .testing import EventLoopMockMixin


class TestUDPConnection(IsolatedAsyncioTestCase, EventLoopMockMixin):
    def setUp(self):
        self._create_loop_mock()
        self.udp_conn = UDPClient("localhost", 8125)
        self.addCleanup(self.udp_conn.close)

    async def test_connect(self):
        await self.udp_conn.connect()
