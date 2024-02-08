import contextlib
import random
from datetime import timedelta
from time import perf_counter as time_now

from ..metrics.basic import (
    CounterMetric,
    GaugeMetric,
    SetMetric,
    StatsdMetric,
    TimingMetric,
)
from .udp import UDPClient


class StatsdClientBase(UDPClient):
    def send(self, data: StatsdMetric):
        serialized = data.serialize()
        if data.rate < 1:
            if random.random() > data.rate:
                return
        super().send(serialized)


class AbstractStatsdClient:
    def timing(self, stat, delta: float | timedelta, rate=1):
        raise NotImplementedError

    def timer(self, stat, rate=1):
        raise NotImplementedError

    def incr(self, stat, count=1, rate=1):
        raise NotImplementedError

    def decr(self, stat, count=1, rate=1):
        raise NotImplementedError

    def gauge(self, stat, value, rate=1, delta=False):
        raise NotImplementedError

    def set(self, stat, value, rate=1):
        raise NotImplementedError


class StatsdClient(AbstractStatsdClient, StatsdClientBase):
    def timing(self, stat, delta: float | timedelta, rate=1):
        """Send new timing information. `delta` is in milliseconds or datetime.timedelta"""
        self.send(TimingMetric(stat, delta, rate=rate))

    def incr(self, stat, count=1, rate=1):
        """Increment a stat by `count`."""
        self.send(CounterMetric(stat, count, rate=rate))

    def decr(self, stat, count=1, rate=1):
        """Decrement a stat by `count`."""
        self.incr(stat, -count, rate=rate)

    def gauge(self, stat, value, rate=1, delta=False):
        """Set a gauge value."""
        self.send(GaugeMetric(stat, value, rate=rate))

    def set(self, stat, value, rate=1):
        """Set a set value."""
        self.send(SetMetric(stat, value, rate=rate))

    @contextlib.contextmanager
    def timer(self, stat, rate=1):
        """Set a timer value via context manager."""
        try:
            start_time = time_now()
            yield
        finally:
            elapsed_time_ms = 1000.0 * (time_now() - start_time)
            self.send(TimingMetric(stat, elapsed_time_ms, rate=rate))
