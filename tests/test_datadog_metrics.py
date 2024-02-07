from unittest import TestCase

from aiostatsd.datadog_metrics import DatadogCounterMetric


class TestCounterMetric(TestCase):
    def test_serialize_full_rate_with_one_tag(self):
        self.counter = DatadogCounterMetric("test", tags=dict(test_tag="test"))
        self.assertEqual(self.counter.serialize(), "test:1|c|#test_tag:test")

    def test_serialize_full_rate_with_two_tags(self):
        self.counter = DatadogCounterMetric("test", tags=dict(test_tag="test", test_tag2="test2"))
        self.assertEqual(self.counter.serialize(), "test:1|c|#test_tag:test,test_tag2:test2")

    def test_serialize_half_rate_with_two_tags(self):
        self.counter = DatadogCounterMetric("test", rate=0.5, tags=dict(test_tag="test", test_tag2="test2"))
        self.assertEqual(self.counter.serialize(), "test:1|c|@0.5|#test_tag:test,test_tag2:test2")

    def test_serialize_half_rate_without_tags(self):
        self.counter = DatadogCounterMetric("test", rate=0.5)
        self.assertEqual(self.counter.serialize(), "test:1|c|@0.5")
