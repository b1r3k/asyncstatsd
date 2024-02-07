from dataclasses import dataclass, field
from typing import Dict

from .basic import GaugeMetricBase, Metric, TimingMetricBase


class DatadogMetricBase(Metric):
    # TODO: remove default for rate attribute, keep it at level of DatadogMetric
    def __init__(self, name: str, value, unit: str, rate: float = 1.0, *, tags: Dict[str, str | int] = None):
        self._tags = tags
        super().__init__(name, value, unit, rate)

    def _build_tags(self) -> str:
        return ",".join(f"{k}:{v}" for k, v in self._tags.items())

    def serialize(self) -> str:
        serialized = super().serialize()
        tag_string = self._build_tags()
        serialized = "|#".join(filter(lambda s: s, [serialized, tag_string]))
        return serialized


@dataclass
class DatadogMetric(DatadogMetricBase):
    name: str
    value: int
    unit: str
    rate: float = field(default=1.0)
    tags: Dict[str, str | int] = field(default_factory=dict)

    def __post_init__(self):
        super().__init__(self.name, self.value, self.unit, self.rate, tags=self.tags)


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
