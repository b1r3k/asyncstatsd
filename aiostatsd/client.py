import contextlib
import random
from datetime import timedelta
from time import perf_counter as time_now
from typing import Union

from .metrics import CounterMetric, GaugeMetric, SetMetric, StatsdMetric, TimingMetric
from .udp import UDPClient


class StatsdClientBase(UDPClient):
    async def send(self, data: StatsdMetric):
        serialized = data.serialize()
        if data.rate < 1:
            if random.random() > data.rate:
                return
        await super().send(serialized)


class StatsdClient(StatsdClientBase):
    async def timing(self, stat, delta: Union[float, timedelta], rate=1):
        """Send new timing information. `delta` is in milliseconds or datetime.timedelta"""
        await self.send(TimingMetric(stat, delta, rate=rate))

    async def incr(self, stat, count=1, rate=1):
        """Increment a stat by `count`."""
        await self.send(CounterMetric(stat, count, rate=rate))

    async def decr(self, stat, count=1, rate=1):
        """Decrement a stat by `count`."""
        await self.incr(stat, -count, rate=rate)

    async def gauge(self, stat, value, rate=1, delta=False):
        """Set a gauge value."""
        await self.send(GaugeMetric(stat, value, rate=rate))

    async def set(self, stat, value, rate=1):
        """Set a set value."""
        await self.send(SetMetric(stat, value, rate=rate))

    @contextlib.asynccontextmanager
    async def timer(self, stat, rate=1):
        """Set a timer value via context manager."""
        try:
            start_time = time_now()
            yield
        finally:
            elapsed_time_ms = 1000.0 * (time_now() - start_time)
            await self.send(TimingMetric(stat, elapsed_time_ms, rate=rate))
