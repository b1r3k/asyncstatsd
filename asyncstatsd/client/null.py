import contextlib

from .basic import AbstractStatsdClient


class NullStatsdClient(AbstractStatsdClient):
    async def connect(self):
        pass

    def close(self):
        pass

    def timing(self, *args, **kwargs):
        pass

    @contextlib.contextmanager
    def timer(self, *args, **kwargs):
        yield

    def incr(self, *args, **kwargs):
        pass

    def decr(self, *args, **kwargs):
        pass

    def gauge(self, *args, **kwargs):
        pass

    def set(self, *args, **kwargs):
        pass
