from dataclasses import dataclass, field
from typing import Dict

from .basic import GaugeMetricBase, StatsdMetric, TimingMetricBase


@dataclass
class DatadogMetric(StatsdMetric):
    tags: Dict[str, str | int] = field(default_factory=dict)

    def _build_tags(self) -> str:
        return ",".join(f"{k}:{v}" for k, v in self.tags.items())

    def serialize(self) -> str:
        serialized = super().serialize()
        tag_string = self._build_tags()
        serialized = "|#".join(filter(lambda s: s, [serialized, tag_string]))
        return serialized


@dataclass
class DatadogCounterMetric(DatadogMetric):
    unit: str = field(default="c", init=False)
    value: int = field(default=1)


@dataclass
class DatadogGaugeMetric(GaugeMetricBase, DatadogMetric):
    unit: str = field(default="g", init=False)
    delta: bool = field(default=False)


@dataclass
class DatadogSetMetric(DatadogMetric):
    unit: str = field(default="s", init=False)


@dataclass
class DatadogTimingMetric(TimingMetricBase, DatadogMetric):
    unit: str = field(default="ms", init=False)
    value: int = field(default=1)
    delta: bool = field(default=False)
