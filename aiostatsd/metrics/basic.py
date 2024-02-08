from dataclasses import dataclass, field
from datetime import timedelta


@dataclass
class StatsdMetric:
    name: str
    value: int
    unit: str
    rate: float = field(default=1.0)

    def get_value(self) -> str:
        return f"{self.value}"

    def serialize(self) -> str | None:
        value = self.get_value()
        serialized = f"{self.name}:{value}|{self.unit}"
        if self.rate < 1:
            serialized = f"{serialized}|@{self.rate}"
        return serialized


@dataclass
class CounterMetric(StatsdMetric):
    unit: str = field(default="c", init=False)
    value: int = field(default=1)


class GaugeMetricBase:
    def get_value(self) -> str:
        value = self.value
        if self.delta:
            sign = "+" if self.value > 0 else ""
            value = f"{sign}{value}"
        return value


@dataclass
class GaugeMetric(GaugeMetricBase, StatsdMetric):
    unit: str = field(default="g", init=False)
    delta: bool = field(default=False)


@dataclass
class SetMetric(StatsdMetric):
    unit: str = field(default="s", init=False)


class TimingMetricBase:
    def get_value(self) -> str:
        delta = self.value
        if isinstance(delta, timedelta):
            # Convert timedelta to number of milliseconds.
            delta = delta.total_seconds() * 1000.0
        return f"{delta:.6f}"


@dataclass
class TimingMetric(TimingMetricBase, StatsdMetric):
    value: float | timedelta
    unit: str = field(default="ms", init=False)
