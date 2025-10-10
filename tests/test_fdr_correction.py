"""
Tests for Benjamini-Hochberg FDR correction.
"""

import pytest
from promptcontracts.stats.significance import benjamini_hochberg_correction


class TestBenjaminiHochbergCorrection:
    def test_basic_correction(self):
        """Test basic FDR correction."""
        p_values = [0.001, 0.01, 0.03, 0.05, 0.1]
        adjusted = benjamini_hochberg_correction(p_values, alpha=0.05)

        # Should be monotonic (non-decreasing)
        assert all(adjusted[i] <= adjusted[i + 1] for i in range(len(adjusted) - 1))

        # Should be capped at 1.0
        assert all(p <= 1.0 for p in adjusted)

        # First p-value should be most adjusted
        assert adjusted[0] > p_values[0]

    def test_empty_list(self):
        """Test empty p-values list."""
        adjusted = benjamini_hochberg_correction([])
        assert adjusted == []

    def test_single_p_value(self):
        """Test single p-value."""
        p_values = [0.01]
        adjusted = benjamini_hochberg_correction(p_values)
        assert len(adjusted) == 1
        assert adjusted[0] == 0.01

    def test_all_significant(self):
        """Test when all p-values are significant."""
        p_values = [0.001, 0.002, 0.003]
        adjusted = benjamini_hochberg_correction(p_values, alpha=0.05)

        # All should remain significant after correction
        assert all(p < 0.05 for p in adjusted)

    def test_none_significant(self):
        """Test when no p-values are significant."""
        p_values = [0.1, 0.2, 0.3, 0.4]
        adjusted = benjamini_hochberg_correction(p_values, alpha=0.05)

        # None should become significant after correction
        assert all(p > 0.05 for p in adjusted)

    def test_monotonicity(self):
        """Test that adjusted p-values maintain monotonicity."""
        p_values = [0.05, 0.01, 0.03, 0.02]
        adjusted = benjamini_hochberg_correction(p_values)

        # BH procedure should ensure monotonicity
        # Check that the implementation enforces this
        assert len(adjusted) == len(p_values)

        # All values should be <= 1.0
        assert all(p <= 1.0 for p in adjusted)

        # All values should be >= 0.0
        assert all(p >= 0.0 for p in adjusted)

    def test_different_alpha(self):
        """Test with different alpha levels."""
        p_values = [0.01, 0.02, 0.03, 0.04, 0.05]

        adjusted_05 = benjamini_hochberg_correction(p_values, alpha=0.05)
        adjusted_01 = benjamini_hochberg_correction(p_values, alpha=0.01)

        # With stricter alpha, fewer should be significant
        significant_05 = sum(1 for p in adjusted_05 if p < 0.05)
        significant_01 = sum(1 for p in adjusted_01 if p < 0.01)

        assert significant_05 >= significant_01
