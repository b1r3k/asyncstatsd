from dataclasses import dataclass, field
from datetime import timedelta
from typing import Dict

from .basic import GaugeMetricMixin, StatsdMetric, TimingMetricMixin


@dataclass
class DatadogMetric(StatsdMetric):
    tags: Dict = field(default_factory=dict)

    def _build_tags(self) -> str:
        return ",".join(f"{k}:{v}" for k, v in self.tags.items())

    def serialize(self) -> str:
        serialized = super().serialize()
        tag_string = self._build_tags()
        serialized = "|#".join(filter(lambda s: s, [serialized, tag_string]))
        return serialized


@dataclass
class DatadogCounterMetric(DatadogMetric):
    unit: str = "c"
    value: int = 1


@dataclass
class DatadogGaugeMetric(GaugeMetricMixin, DatadogMetric):
    unit: str = "g"
    delta: bool = False


@dataclass
class DatadogSetMetric(DatadogMetric):
    unit: str = "s"


@dataclass
class DatadogTimingMetric(TimingMetricMixin, DatadogMetric):
    unit: str = "ms"
    value: int | float | timedelta
