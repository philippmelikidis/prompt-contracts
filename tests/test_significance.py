"""
Tests for significance testing methods.
"""

import pytest
from promptcontracts.stats.significance import bootstrap_diff_ci, mcnemar_test


class TestMcNemarTest:
    def test_mcnemar_no_disagreement(self):
        """Test McNemar when no disagreements."""
        p_value = mcnemar_test(a01=0, a10=0)
        assert p_value == 1.0  # Perfect agreement

    def test_mcnemar_symmetric_disagreement(self):
        """Test McNemar with equal disagreements."""
        p_value = mcnemar_test(a01=10, a10=10)
        assert p_value > 0.8  # High p-value (no difference)

    def test_mcnemar_asymmetric_disagreement(self):
        """Test McNemar with asymmetric disagreements."""
        p_value = mcnemar_test(a01=20, a10=5)
        assert p_value < 0.01  # Significant difference

    def test_mcnemar_continuity_correction(self):
        """Test McNemar with and without continuity correction."""
        a01, a10 = 15, 8
        p_with = mcnemar_test(a01, a10, continuity_correction=True)
        p_without = mcnemar_test(a01, a10, continuity_correction=False)

        # With correction should give higher (more conservative) p-value
        assert p_with >= p_without

    def test_mcnemar_small_sample(self):
        """Test McNemar with small disagreements."""
        p_value = mcnemar_test(a01=3, a10=1, continuity_correction=True)
        assert 0.1 < p_value < 1.0  # Not significant with small sample


class TestBootstrapDiffCI:
    def test_bootstrap_diff_no_difference(self):
        """Test bootstrap diff CI when metrics are identical."""
        metric1 = [100, 120, 110, 105, 115, 108, 112, 118, 103, 107]
        metric2 = [100, 120, 110, 105, 115, 108, 112, 118, 103, 107]

        lower, upper = bootstrap_diff_ci(metric1, metric2, B=1000, seed=42)

        # CI should contain 0
        assert lower <= 0 <= upper
        # CI should be narrow
        assert abs(upper - lower) < 5

    def test_bootstrap_diff_positive_difference(self):
        """Test bootstrap diff CI when metric2 > metric1."""
        metric1 = [100, 105, 110, 108, 112]
        metric2 = [150, 155, 160, 158, 162]  # ~50 higher

        lower, upper = bootstrap_diff_ci(metric1, metric2, B=1000, seed=42)

        # CI should not contain 0, and both bounds positive
        assert lower > 0
        assert upper > 0
        assert 40 < lower <= 50
        assert 50 <= upper < 60

    def test_bootstrap_diff_negative_difference(self):
        """Test bootstrap diff CI when metric2 < metric1."""
        metric1 = [200, 210, 205, 215, 208]
        metric2 = [150, 160, 155, 165, 158]  # ~50 lower

        lower, upper = bootstrap_diff_ci(metric1, metric2, B=1000, seed=42)

        # CI should not contain 0, and both bounds negative
        assert lower < 0
        assert upper < 0
        assert -60 < lower <= -50
        assert -50 <= upper < -40

    def test_bootstrap_diff_mismatched_length(self):
        """Test bootstrap diff CI with mismatched lengths."""
        metric1 = [100, 110, 120]
        metric2 = [105, 115]

        with pytest.raises(ValueError, match="same length"):
            bootstrap_diff_ci(metric1, metric2, B=100)

    def test_bootstrap_diff_empty(self):
        """Test bootstrap diff CI with empty metrics."""
        lower, upper = bootstrap_diff_ci([], [], B=100, seed=42)
        assert lower == 0.0
        assert upper == 0.0

    def test_bootstrap_diff_reproducibility(self):
        """Test bootstrap diff reproducibility with same seed."""
        metric1 = [100, 110, 120, 105, 115]
        metric2 = [105, 115, 125, 110, 120]

        ci1 = bootstrap_diff_ci(metric1, metric2, B=1000, seed=42)
        ci2 = bootstrap_diff_ci(metric1, metric2, B=1000, seed=42)

        assert ci1 == ci2

    def test_bootstrap_diff_confidence_level(self):
        """Test bootstrap diff with different confidence levels."""
        metric1 = [100, 110, 120, 105, 115, 108, 112, 118, 103, 107]
        metric2 = [105, 115, 125, 110, 120, 113, 117, 123, 108, 112]

        ci_95 = bootstrap_diff_ci(metric1, metric2, B=1000, alpha=0.05, seed=42)
        ci_99 = bootstrap_diff_ci(metric1, metric2, B=1000, alpha=0.01, seed=42)

        # 99% CI should be wider than or equal to 95% CI
        width_95 = ci_95[1] - ci_95[0]
        width_99 = ci_99[1] - ci_99[0]
        assert width_99 >= width_95


class TestSignificancePracticalExamples:
    def test_system_comparison_significant(self):
        """Realistic example: comparing two systems with significant difference."""
        # System A: 80/100 pass, System B: 90/100 pass
        # Disagreements: A passed but B failed: 5, A failed but B passed: 15
        a01 = 15
        a10 = 5

        p_value = mcnemar_test(a01, a10)
        assert p_value < 0.05  # Significant difference

    def test_system_comparison_not_significant(self):
        """Realistic example: comparing two systems without significant difference."""
        # System A: 85/100 pass, System B: 87/100 pass
        # Disagreements: A passed but B failed: 3, A failed but B passed: 5
        a01 = 5
        a10 = 3

        p_value = mcnemar_test(a01, a10)
        assert p_value > 0.05  # Not significant

    def test_latency_comparison(self):
        """Realistic example: comparing latencies."""
        # System A latencies (ms)
        latencies_a = [120, 135, 128, 142, 131, 125, 138, 145, 122, 140]
        # System B latencies (ms) - faster
        latencies_b = [110, 125, 118, 132, 121, 115, 128, 135, 112, 130]

        lower, upper = bootstrap_diff_ci(latencies_a, latencies_b, B=1000, seed=42)

        # B is faster, so difference (B - A) should be negative
        assert upper < 0  # Significantly faster
        assert -20 < lower < -5  # Reasonable improvement range
