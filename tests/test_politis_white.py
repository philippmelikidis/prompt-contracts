"""
Tests for Politis-White block size estimator.
"""

import numpy as np
import pytest
from promptcontracts.stats.intervals import politis_white_block_size


class TestPolitisWhiteBlockSize:
    def test_basic_estimation(self):
        """Test basic block size estimation."""
        # Generate AR(1) process with known correlation
        np.random.seed(42)
        n = 100
        phi = 0.5
        data = np.zeros(n)
        data[0] = np.random.randn()
        for i in range(1, n):
            data[i] = phi * data[i - 1] + np.random.randn()

        block_size = politis_white_block_size(data)

        # Should return reasonable block size
        assert 2 <= block_size <= 50
        assert isinstance(block_size, int)

    def test_small_sample(self):
        """Test with very small sample."""
        data = np.array([1, 2, 3])
        block_size = politis_white_block_size(data)

        # Should handle small samples gracefully
        assert block_size <= len(data)
        assert block_size >= 2

    def test_independent_data(self):
        """Test with independent (white noise) data."""
        np.random.seed(42)
        data = np.random.randn(100)

        block_size = politis_white_block_size(data)

        # For independent data, block size should be small
        assert block_size <= 10

    def test_highly_correlated_data(self):
        """Test with highly correlated data."""
        np.random.seed(42)
        n = 100
        phi = 0.9  # High correlation
        data = np.zeros(n)
        data[0] = np.random.randn()
        for i in range(1, n):
            data[i] = phi * data[i - 1] + np.random.randn()

        block_size = politis_white_block_size(data)

        # Should suggest larger block size for correlated data
        assert block_size >= 5

    def test_max_block_size_constraint(self):
        """Test max block size constraint."""
        np.random.seed(42)
        data = np.random.randn(200)

        block_size = politis_white_block_size(data, max_block_size=10)

        # Should respect max constraint
        assert block_size <= 10

    def test_deterministic_with_seed(self):
        """Test that results are deterministic with same seed."""
        np.random.seed(42)
        data1 = np.random.randn(100)
        block_size1 = politis_white_block_size(data1)

        np.random.seed(42)
        data2 = np.random.randn(100)
        block_size2 = politis_white_block_size(data2)

        # Should be identical with same seed
        assert block_size1 == block_size2

    def test_edge_cases(self):
        """Test edge cases."""
        # Very short data
        data_short = np.array([1, 2])
        block_size_short = politis_white_block_size(data_short)
        assert block_size_short <= 2

        # Constant data
        data_constant = np.ones(50)
        block_size_constant = politis_white_block_size(data_constant)
        assert 2 <= block_size_constant <= 50

    def test_auto_block_integration(self):
        """Test integration with percentile_bootstrap_ci."""
        from promptcontracts.stats.intervals import percentile_bootstrap_ci

        np.random.seed(42)
        # Use binary data (0s and 1s) for proportion estimation
        data = np.random.choice([0, 1], size=50, p=[0.3, 0.7])

        # Should work with auto_block=True
        ci_lower, ci_upper = percentile_bootstrap_ci(data.tolist(), B=100, auto_block=True, seed=42)

        assert ci_lower < ci_upper
        assert 0 <= ci_lower <= 1
        assert 0 <= ci_upper <= 1
