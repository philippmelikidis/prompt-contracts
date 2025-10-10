"""
Tests for power analysis methods.
"""

import pytest
from promptcontracts.stats.power import effect_size_cohens_h, required_n_for_proportion


class TestRequiredN:
    def test_medium_effect(self):
        """Test required n for detecting medium effect."""
        n = required_n_for_proportion(p0=0.5, p1=0.7, alpha=0.05, power=0.8)
        # For medium effect, typically ~50-80 samples
        assert 40 < n < 100

    def test_small_effect(self):
        """Test required n for detecting small effect."""
        n = required_n_for_proportion(p0=0.80, p1=0.85, alpha=0.05, power=0.8)
        # Small effect requires larger n
        assert n > 200

    def test_large_effect(self):
        """Test required n for detecting large effect."""
        n = required_n_for_proportion(p0=0.5, p1=0.8, alpha=0.05, power=0.8)
        # Large effect requires smaller n
        assert n < 50

    def test_higher_power(self):
        """Test that higher power requires larger n."""
        n_80 = required_n_for_proportion(p0=0.6, p1=0.75, alpha=0.05, power=0.8)
        n_90 = required_n_for_proportion(p0=0.6, p1=0.75, alpha=0.05, power=0.9)

        assert n_90 > n_80

    def test_lower_alpha(self):
        """Test that lower alpha (more stringent) requires larger n."""
        n_05 = required_n_for_proportion(p0=0.6, p1=0.75, alpha=0.05, power=0.8)
        n_01 = required_n_for_proportion(p0=0.6, p1=0.75, alpha=0.01, power=0.8)

        assert n_01 > n_05

    def test_symmetric_effect(self):
        """Test that effect size matters, not direction."""
        n_increase = required_n_for_proportion(p0=0.5, p1=0.6, alpha=0.05, power=0.8)
        n_decrease = required_n_for_proportion(p0=0.6, p1=0.5, alpha=0.05, power=0.8)

        # Should be approximately equal (within rounding)
        assert abs(n_increase - n_decrease) <= 1

    def test_invalid_proportions(self):
        """Test error handling for invalid proportions."""
        with pytest.raises(ValueError, match="between 0 and 1"):
            required_n_for_proportion(p0=1.5, p1=0.8)

        with pytest.raises(ValueError, match="between 0 and 1"):
            required_n_for_proportion(p0=0.5, p1=-0.2)

    def test_equal_proportions(self):
        """Test error handling when p0 == p1."""
        with pytest.raises(ValueError, match="must differ"):
            required_n_for_proportion(p0=0.7, p1=0.7)


class TestCohensH:
    def test_no_difference(self):
        """Test Cohen's h when proportions are equal."""
        h = effect_size_cohens_h(0.5, 0.5)
        assert h == 0.0

    def test_small_effect(self):
        """Test small effect size (h < 0.2)."""
        h = effect_size_cohens_h(0.50, 0.55)
        assert h < 0.2

    def test_medium_effect(self):
        """Test medium effect size (0.2 <= h < 0.5)."""
        h = effect_size_cohens_h(0.50, 0.70)
        assert 0.2 <= h < 0.5

    def test_large_effect(self):
        """Test large effect size (h >= 0.5)."""
        h = effect_size_cohens_h(0.30, 0.70)
        assert h >= 0.5

    def test_extreme_difference(self):
        """Test extreme difference in proportions."""
        h = effect_size_cohens_h(0.10, 0.90)
        assert h > 1.0

    def test_symmetric(self):
        """Test that Cohen's h is symmetric."""
        h1 = effect_size_cohens_h(0.4, 0.6)
        h2 = effect_size_cohens_h(0.6, 0.4)
        assert h1 == pytest.approx(h2, abs=1e-10)

    def test_boundary_zero(self):
        """Test at zero boundary."""
        h = effect_size_cohens_h(0.0, 0.5)
        assert h > 0
        # arcsin(0) = 0, arcsin(sqrt(0.5)) ≈ 0.785
        # h = 2 * 0.785 ≈ 1.57
        assert 1.5 < h < 1.6

    def test_boundary_one(self):
        """Test at one boundary."""
        h = effect_size_cohens_h(0.5, 1.0)
        assert h > 0
        # arcsin(sqrt(0.5)) ≈ 0.785, arcsin(sqrt(1.0)) = π/2 ≈ 1.571
        # h = 2 * |1.571 - 0.785| ≈ 1.57
        assert 1.5 < h < 1.6

    def test_invalid_proportions(self):
        """Test error handling for invalid proportions."""
        with pytest.raises(ValueError, match="must be in"):
            effect_size_cohens_h(-0.1, 0.5)

        with pytest.raises(ValueError, match="must be in"):
            effect_size_cohens_h(0.5, 1.5)


class TestPowerAnalysisPractical:
    def test_pcsl_typical_scenario(self):
        """Test realistic PCSL scenario: detect 10% improvement."""
        # Baseline: 85% validation success
        # Target: 95% validation success
        # Want to detect this difference with 80% power
        n = required_n_for_proportion(p0=0.85, p1=0.95, alpha=0.05, power=0.8)

        # This is a moderate effect, should need ~100-200 samples
        assert 80 < n < 250

    def test_effect_size_interpretation(self):
        """Test effect size interpretation for PCSL scenarios."""
        # Small improvement: 85% -> 88%
        h_small = effect_size_cohens_h(0.85, 0.88)
        assert h_small < 0.2  # Small effect

        # Medium improvement: 75% -> 85%
        h_medium = effect_size_cohens_h(0.75, 0.85)
        assert 0.2 <= h_medium < 0.5  # Medium effect

        # Large improvement: 60% -> 85%
        h_large = effect_size_cohens_h(0.60, 0.85)
        assert h_large >= 0.5  # Large effect

    def test_underpowered_study(self):
        """Test detecting underpowered study."""
        # Very small sample with small effect
        n_needed = required_n_for_proportion(p0=0.85, p1=0.88, alpha=0.05, power=0.8)

        # If we only have 50 samples, we're likely underpowered
        assert n_needed > 50  # Confirms we need more than 50

    def test_well_powered_study(self):
        """Test well-powered study design."""
        # Large effect with adequate sample
        n_needed = required_n_for_proportion(p0=0.6, p1=0.8, alpha=0.05, power=0.8)

        # If we have 100 samples, we should be well-powered
        assert n_needed < 100  # Confirms 100 is sufficient
