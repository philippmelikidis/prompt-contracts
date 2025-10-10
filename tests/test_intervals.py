"""
Tests for confidence interval methods.
"""

import pytest
from promptcontracts.stats.intervals import (
    jeffreys_interval,
    percentile_bootstrap_ci,
    wilson_interval,
)


class TestWilsonInterval:
    def test_wilson_basic(self):
        """Test Wilson interval for typical case."""
        lower, upper = wilson_interval(85, 100, confidence=0.95)
        assert 0.75 < lower < 0.80
        assert 0.90 < upper < 0.95

    def test_wilson_perfect_success(self):
        """Test Wilson interval when all successes."""
        lower, upper = wilson_interval(100, 100, confidence=0.95)
        assert lower > 0.95  # High lower bound
        assert upper == 1.0

    def test_wilson_perfect_failure(self):
        """Test Wilson interval when all failures."""
        lower, upper = wilson_interval(0, 100, confidence=0.95)
        assert lower < 0.001  # Nearly zero (floating point tolerance)
        assert upper < 0.05  # Low upper bound

    def test_wilson_small_n(self):
        """Test Wilson interval with small n."""
        lower, upper = wilson_interval(8, 10, confidence=0.95)
        assert 0.4 < lower < 0.6
        assert 0.9 < upper < 1.0

    def test_wilson_zero_n(self):
        """Test Wilson interval with n=0."""
        lower, upper = wilson_interval(0, 0, confidence=0.95)
        assert lower == 0.0
        assert upper == 1.0


class TestJeffreysInterval:
    def test_jeffreys_basic(self):
        """Test Jeffreys interval for typical case."""
        lower, upper = jeffreys_interval(7, 10, confidence=0.95)
        assert 0.3 < lower < 0.5
        assert 0.85 < upper < 0.98

    def test_jeffreys_boundary_zero(self):
        """Test Jeffreys interval at zero boundary."""
        lower, upper = jeffreys_interval(0, 10, confidence=0.95)
        assert lower == 0.0
        assert 0.2 < upper < 0.4

    def test_jeffreys_boundary_n(self):
        """Test Jeffreys interval at n boundary."""
        lower, upper = jeffreys_interval(10, 10, confidence=0.95)
        assert 0.6 < lower < 0.8
        assert upper == 1.0

    def test_jeffreys_zero_n(self):
        """Test Jeffreys interval with n=0."""
        lower, upper = jeffreys_interval(0, 0, confidence=0.95)
        assert lower == 0.0
        assert upper == 1.0


class TestPercentileBootstrap:
    def test_bootstrap_basic(self):
        """Test bootstrap CI for typical binary data."""
        values = [1, 1, 0, 1, 1, 0, 1, 1, 1, 0]  # 7/10 success
        lower, upper = percentile_bootstrap_ci(values, B=1000, seed=42)
        assert 0.3 < lower < 0.6
        assert 0.8 < upper < 1.0

    def test_bootstrap_perfect_success(self):
        """Test bootstrap CI when all successes."""
        values = [1] * 20
        lower, upper = percentile_bootstrap_ci(values, B=1000, seed=42)
        assert lower == 1.0
        assert upper == 1.0

    def test_bootstrap_block(self):
        """Test block bootstrap for dependent data."""
        values = [1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0]  # Blocked pattern
        lower_standard, upper_standard = percentile_bootstrap_ci(
            values, B=1000, block=None, seed=42
        )
        lower_block, upper_block = percentile_bootstrap_ci(values, B=1000, block=3, seed=42)

        # Block bootstrap should give wider CI for dependent data
        assert lower_block <= lower_standard or upper_block >= upper_standard

    def test_bootstrap_empty(self):
        """Test bootstrap CI with empty data."""
        lower, upper = percentile_bootstrap_ci([], B=100, seed=42)
        assert lower == 0.0
        assert upper == 1.0

    def test_bootstrap_reproducibility(self):
        """Test bootstrap reproducibility with same seed."""
        values = [1, 0, 1, 1, 0, 1, 0, 1, 1, 0]
        ci1 = percentile_bootstrap_ci(values, B=1000, seed=42)
        ci2 = percentile_bootstrap_ci(values, B=1000, seed=42)
        assert ci1 == ci2


class TestIntervalComparison:
    def test_wilson_vs_jeffreys_large_n(self):
        """For large n, Wilson and Jeffreys should be similar."""
        successes, n = 85, 100
        wilson_ci = wilson_interval(successes, n)
        jeffreys_ci = jeffreys_interval(successes, n)

        # Should be within 0.05 of each other
        assert abs(wilson_ci[0] - jeffreys_ci[0]) < 0.05
        assert abs(wilson_ci[1] - jeffreys_ci[1]) < 0.05

    def test_wilson_vs_bootstrap(self):
        """Wilson and bootstrap should agree reasonably."""
        successes, n = 70, 100
        values = [1] * successes + [0] * (n - successes)

        wilson_ci = wilson_interval(successes, n)
        bootstrap_ci = percentile_bootstrap_ci(values, B=2000, seed=42)

        # Should be within 0.1 of each other
        assert abs(wilson_ci[0] - bootstrap_ci[0]) < 0.1
        assert abs(wilson_ci[1] - bootstrap_ci[1]) < 0.1
