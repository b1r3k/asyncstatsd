from unittest import IsolatedAsyncioTestCase

from asyncstatsd.client import NullStatsdClient


class TestNullStatsdClient(IsolatedAsyncioTestCase):
    async def test_null_client(self):
        client = NullStatsdClient()
        await client.connect()
        client.incr("test")
        client.decr("test")
        client.gauge("test", 30)
        client.set("test", 30)
        client.timing("test", 100)
        with client.timer("test"):
            pass
        client.close()
