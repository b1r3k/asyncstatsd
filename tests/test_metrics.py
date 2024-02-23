from unittest import TestCase

from asyncstatsd.metrics.basic import (
    CounterMetric,
    GaugeMetric,
    SetMetric,
    TimingMetric,
)


class TestCounterMetric(TestCase):
    def test_serialize_full_rate(self):
        self.counter = CounterMetric("test")
        self.assertEqual(self.counter.serialize(), "test:1|c")

    def test_serialize_half_rate(self):
        self.counter = CounterMetric("test", rate=0.5)
        self.assertEqual(self.counter.serialize(), "test:1|c|@0.5")


class TestGaugeMetric(TestCase):
    def setUp(self):
        self.gauge = GaugeMetric("test", 30)

    def test_serialize_full_rate(self):
        self.assertEqual(self.gauge.serialize(), "test:30|g")

    def test_serialize_half_rate(self):
        self.gauge = GaugeMetric("test", 30, rate=0.5)
        self.assertEqual(self.gauge.serialize(), "test:30|g|@0.5")

    def test_serialize_delta_full_rate(self):
        self.gauge = GaugeMetric("test", -30, delta=True)
        self.assertEqual(self.gauge.serialize(), "test:-30|g")

    def test_serialize_delta_half_rate(self):
        self.gauge = GaugeMetric("test", 30, rate=0.5, delta=True)
        self.assertEqual(self.gauge.serialize(), "test:+30|g|@0.5")


class TestTimingMetric(TestCase):
    def setUp(self):
        self.timing = TimingMetric("test", 100)

    def test_serialize_full_rate(self):
        self.assertEqual(self.timing.serialize(), "test:100.000000|ms")

    def test_serialize_half_rate(self):
        self.timing = TimingMetric("test", 100, rate=0.5)
        self.assertEqual(self.timing.serialize(), "test:100.000000|ms|@0.5")


class TestSetMetric(TestCase):
    def test_serialize_full_rate(self):
        self.set = SetMetric("test", 30)
        self.assertEqual(self.set.serialize(), "test:30|s")

    def test_serialize_half_rate(self):
        self.set = SetMetric("test", 30, rate=0.5)
        self.assertEqual(self.set.serialize(), "test:30|s|@0.5")
