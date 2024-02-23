from dataclasses import dataclass, field
from datetime import timedelta


@dataclass
class StatsdMetric:
    name: str
    value: int | float | timedelta
    unit: str
    rate: float = field(default=1.0)

    def get_value(self) -> str:
        return f"{self.value}"

    def serialize(self) -> str:
        value = self.get_value()
        serialized = f"{self.name}:{value}|{self.unit}"
        if self.rate < 1:
            serialized = f"{serialized}|@{self.rate}"
        return serialized


@dataclass
class CounterMetric(StatsdMetric):
    unit: str = "c"
    value: int = 1


class GaugeMetricMixin:
    def get_value(self) -> str:
        value = self.value  # type: ignore
        if self.delta:  # type: ignore
            sign = "+" if value > 0 else ""
            value = f"{sign}{value}"
        return str(value)


@dataclass
class GaugeMetric(GaugeMetricMixin, StatsdMetric):
    unit: str = "g"
    delta: bool = False


@dataclass
class SetMetric(StatsdMetric):
    unit: str = "s"


class TimingMetricMixin:
    def get_value(self) -> str:
        delta = self.value  # type: ignore
        if isinstance(delta, timedelta):
            # Convert timedelta to number of milliseconds.
            delta = delta.total_seconds() * 1000.0
        return f"{delta:.6f}"


@dataclass
class TimingMetric(TimingMetricMixin, StatsdMetric):
    value: float | timedelta
    unit: str = "ms"
