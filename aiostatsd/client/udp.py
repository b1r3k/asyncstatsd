import asyncio
import logging

logger = logging.getLogger()


class StatsdProtocol(asyncio.DatagramProtocol):
    def __init__(self, on_con_lost: asyncio.Future | None = None):
        self.on_con_lost = on_con_lost
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        print("Connection made")

    def error_received(self, exc):
        print("Error received:", exc)

    def connection_lost(self, exc):
        if self.on_con_lost is not None:
            self.on_con_lost.set_exception(exc)
        print("Closing transport", exc)


class Client:
    async def connect(self):
        raise NotImplementedError

    async def send(self, data):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError


class UDPClient:
    def __init__(self, host, port, maxudpsize=512):
        self._host = host
        self._port = port
        self._maxudpsize = maxudpsize
        self._loop = asyncio.get_event_loop()
        self._transport = None
        self._on_con_lost = None

    def close(self):
        if self._transport:
            self._transport.close()
            self._transport = None

    async def connect(self):
        self._on_con_lost = self._loop.create_future()
        self._transport, _ = await self._loop.create_datagram_endpoint(
            lambda: StatsdProtocol(self._on_con_lost), remote_addr=(self._host, self._port)
        )
        self._on_con_lost.add_done_callback(lambda f: self._close())

    def send(self, data):
        encoded = data.encode("ascii")
        if len(encoded) > self._maxudpsize:
            logger.warning("Data exceeds max UDP size: %s", data)
        self._transport.sendto(encoded)
