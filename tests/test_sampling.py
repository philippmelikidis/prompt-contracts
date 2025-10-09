"""Tests for sampling module."""

import pytest
from promptcontracts.core.sampling import SampleResult, create_sampler


def test_create_sampler():
    """Test sampler creation."""
    sampler = create_sampler(n=3, seed=42, aggregation="majority")
    assert sampler.config.n == 3
    assert sampler.config.seed == 42
    assert sampler.config.aggregation == "majority"


def test_sampler_first_aggregation():
    """Test first aggregation policy."""
    sampler = create_sampler(n=3, aggregation="first", bootstrap_samples=0)

    samples = [
        SampleResult(0, "output1", None, 100.0, True, []),
        SampleResult(1, "output2", None, 110.0, False, []),
        SampleResult(2, "output3", None, 120.0, True, []),
    ]

    result = sampler.aggregate(samples)
    assert result.selected_output == "output1"
    assert result.all_passed is True
    assert result.pass_rate == 2 / 3


def test_sampler_majority_aggregation():
    """Test majority aggregation policy."""
    sampler = create_sampler(n=5, aggregation="majority", bootstrap_samples=0)

    samples = [
        SampleResult(0, "output_a", None, 100.0, True, []),
        SampleResult(1, "output_a", None, 105.0, True, []),
        SampleResult(2, "output_a", None, 110.0, True, []),
        SampleResult(3, "output_b", None, 115.0, False, []),
        SampleResult(4, "output_b", None, 120.0, False, []),
    ]

    result = sampler.aggregate(samples)
    assert result.selected_output == "output_a"
    assert result.aggregation_metadata["majority_count"] == 3
    assert result.pass_rate == 3 / 5


def test_sampler_all_aggregation():
    """Test all aggregation policy."""
    sampler = create_sampler(n=3, aggregation="all", bootstrap_samples=0)

    # All pass
    samples_pass = [
        SampleResult(0, "output1", None, 100.0, True, []),
        SampleResult(1, "output2", None, 110.0, True, []),
        SampleResult(2, "output3", None, 120.0, True, []),
    ]

    result = sampler.aggregate(samples_pass)
    assert result.all_passed is True

    # One fails
    samples_fail = [
        SampleResult(0, "output1", None, 100.0, True, []),
        SampleResult(1, "output2", None, 110.0, False, []),
        SampleResult(2, "output3", None, 120.0, True, []),
    ]

    result = sampler.aggregate(samples_fail)
    assert result.all_passed is False


def test_sampler_any_aggregation():
    """Test any aggregation policy."""
    sampler = create_sampler(n=3, aggregation="any", bootstrap_samples=0)

    # At least one passes
    samples_pass = [
        SampleResult(0, "output1", None, 100.0, False, []),
        SampleResult(1, "output2", None, 110.0, True, []),
        SampleResult(2, "output3", None, 120.0, False, []),
    ]

    result = sampler.aggregate(samples_pass)
    assert result.all_passed is True
    assert result.selected_output == "output2"

    # None pass
    samples_fail = [
        SampleResult(0, "output1", None, 100.0, False, []),
        SampleResult(1, "output2", None, 110.0, False, []),
        SampleResult(2, "output3", None, 120.0, False, []),
    ]

    result = sampler.aggregate(samples_fail)
    assert result.all_passed is False


def test_bootstrap_ci():
    """Test bootstrap confidence interval calculation."""
    sampler = create_sampler(n=3, bootstrap_samples=100, confidence_level=0.95)

    samples = [
        SampleResult(0, "output1", None, 100.0, True, []),
        SampleResult(1, "output2", None, 110.0, True, []),
        SampleResult(2, "output3", None, 120.0, False, []),
    ]

    result = sampler.aggregate(samples)
    assert result.confidence_interval is not None
    assert len(result.confidence_interval) == 2
    assert 0.0 <= result.confidence_interval[0] <= 1.0
    assert 0.0 <= result.confidence_interval[1] <= 1.0


def test_sample_n():
    """Test sample_n method."""
    sampler = create_sampler(n=3, seed=42, bootstrap_samples=0)

    counter = [0]

    def generator(sample_id: int) -> SampleResult:
        counter[0] += 1
        return SampleResult(sample_id, f"output{sample_id}", None, 100.0, True, [])

    result = sampler.sample_n(generator)
    assert counter[0] == 3
    assert len(result.samples) == 3
