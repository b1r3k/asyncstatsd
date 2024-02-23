import asyncio
import logging
from abc import ABC, abstractmethod

logger = logging.getLogger()


class StatsdProtocol(asyncio.DatagramProtocol):
    def __init__(self, on_con_lost: asyncio.Future | None = None):
        self.on_con_lost = on_con_lost
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        logger.debug("Statsd UDP connection established")

    def error_received(self, exc):
        logger.error("Error received: %s", exc)

    def connection_lost(self, exc):
        if exc and self.on_con_lost:
            self.on_con_lost.set_exception(exc)
        elif self.on_con_lost:
            self.on_con_lost.set_result(True)
        logger.warning("Statsd UDP connection lost")


class Client(ABC):
    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def send(self, data):
        pass

    @abstractmethod
    def close(self):
        pass


class UDPClient:
    def __init__(self, host, port, *, maxudpsize=512):
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
        self._on_con_lost.add_done_callback(lambda f: self.close())

    def send(self, data):
        encoded = data.encode("ascii")
        if len(encoded) > self._maxudpsize:
            logger.warning("Data exceeds max UDP size: %s", data)
        self._transport.sendto(encoded)
