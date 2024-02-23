from datetime import timedelta
from typing import Dict

from ..metrics.datadog import (
    DatadogCounterMetric,
    DatadogGaugeMetric,
    DatadogSetMetric,
    DatadogTimingMetric,
)
from .basic import AbstractStatsdClient, StatsdClientBase


class DatadogClient(AbstractStatsdClient, StatsdClientBase):
    def incr(self, stat, count=1, rate=1, *, tags: Dict = {}):
        """Increment a stat by `count`."""
        self.send(DatadogCounterMetric(stat, count, rate=rate, tags=tags))

    def decr(self, stat, count=1, rate=1, *, tags: Dict = {}):
        """Decrement a stat by `count`."""
        self.incr(stat, -count, rate=rate, tags=tags)

    def gauge(self, stat, value, rate=1, *, delta=False, tags: Dict = {}):
        """Set a gauge value."""
        self.send(DatadogGaugeMetric(stat, value, rate=rate, delta=delta, tags=tags))

    def set(self, stat, value, rate=1, *, tags: Dict = {}):
        """Set a set value."""
        self.send(DatadogSetMetric(stat, value, rate=rate, tags=tags))

    def timing(self, stat, delta: float | timedelta, rate=1, *, tags: Dict = {}):
        """Send new timing information. `delta` is in milliseconds or datetime.timedelta"""
        self.send(DatadogTimingMetric(stat, delta, rate=rate, tags=tags))
