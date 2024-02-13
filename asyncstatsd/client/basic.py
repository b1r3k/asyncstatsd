import contextlib
import random
from abc import ABC, abstractmethod
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
    def __init__(self, host, port, *, maxudpsize=512, prefix: str = ""):
        super().__init__(host, port, maxudpsize=maxudpsize)
        self._prefix = prefix

    def send(self, data: StatsdMetric):
        serialized = "".join([self._prefix, data.serialize()])  # type: ignore
        if data.rate < 1:
            if random.random() > data.rate:
                return
        super().send(serialized)


class AbstractStatsdClient(ABC):
    @abstractmethod
    def timing(self, stat, delta: float | timedelta, rate=1):
        pass

    @contextlib.contextmanager
    def timer(self, stat, rate=1):
        """Set a timer value via context manager."""
        try:
            start_time = time_now()
            yield
        finally:
            elapsed_time_ms = 1000.0 * (time_now() - start_time)
            self.timing(stat, elapsed_time_ms, rate=rate)

    @abstractmethod
    def incr(self, stat, count=1, rate=1):
        pass

    @abstractmethod
    def decr(self, stat, count=1, rate=1):
        pass

    @abstractmethod
    def gauge(self, stat, value, rate=1, delta=False):
        pass

    @abstractmethod
    def set(self, stat, value, rate=1):
        pass


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
