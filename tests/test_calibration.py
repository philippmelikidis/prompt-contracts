"""
Tests for CI calibration module.
"""

import numpy as np
import pytest

from promptcontracts.stats.calibration import (
    calibrate_ci_coverage,
    compare_ci_methods,
    generate_calibration_report,
)


class TestCICalibration:
    def test_wilson_calibration(self):
        """Test Wilson interval calibration."""
        results = calibrate_ci_coverage("wilson", n_sims=1000, seed=42)

        assert "empirical_coverage" in results
        assert "coverage_error" in results
        assert "mean_ci_width" in results
        assert results["method"] == "wilson"
        assert results["nominal_coverage"] == 0.95

        # Empirical coverage should be close to nominal
        assert 0.9 <= results["empirical_coverage"] <= 1.0

    def test_jeffreys_calibration(self):
        """Test Jeffreys interval calibration."""
        results = calibrate_ci_coverage("jeffreys", n_sims=1000, seed=42)

        assert results["method"] == "jeffreys"
        assert 0.9 <= results["empirical_coverage"] <= 1.0

    def test_bootstrap_calibration(self):
        """Test bootstrap interval calibration."""
        results = calibrate_ci_coverage("bootstrap", n_sims=1000, seed=42)

        assert results["method"] == "bootstrap"
        assert 0.9 <= results["empirical_coverage"] <= 1.0

    def test_compare_methods(self):
        """Test method comparison."""
        results = compare_ci_methods(n_sims=1000, seed=42)

        assert "methods" in results
        assert "best_method" in results
        assert "summary" in results

        # Should have results for all methods
        assert len(results["methods"]) >= 2

        # Best method should be defined
        assert results["best_method"] in results["methods"]

    def test_calibration_report(self):
        """Test calibration report generation."""
        report = generate_calibration_report(n_sims=1000, seed=42)

        assert isinstance(report, str)
        assert "CI Calibration Report" in report
        assert "Empirical Coverage" in report
        assert "Best Method" in report

    def test_different_confidence_levels(self):
        """Test calibration with different confidence levels."""
        results_95 = calibrate_ci_coverage("wilson", n_sims=1000, confidence=0.95, seed=42)
        results_99 = calibrate_ci_coverage("wilson", n_sims=1000, confidence=0.99, seed=42)

        assert results_95["nominal_coverage"] == 0.95
        assert results_99["nominal_coverage"] == 0.99

        # 99% CI should be wider
        assert results_99["mean_ci_width"] > results_95["mean_ci_width"]

    def test_edge_cases_tracking(self):
        """Test that edge cases are properly tracked."""
        results = calibrate_ci_coverage("wilson", n_sims=1000, seed=42)

        assert "edge_cases" in results
        edge_cases = results["edge_cases"]

        assert "n_small" in edge_cases
        assert "p_extreme" in edge_cases
        assert "boundary" in edge_cases

        # Should be non-negative counts
        assert all(count >= 0 for count in edge_cases.values())

    def test_calibration_status(self):
        """Test calibration status classification."""
        results = calibrate_ci_coverage("wilson", n_sims=1000, seed=42)

        assert "calibration_status" in results
        assert results["calibration_status"] in ["good", "poor"]

        # Good calibration if error < 2%
        if abs(results["coverage_error"]) < 0.02:
            assert results["calibration_status"] == "good"

    def test_reproducibility(self):
        """Test that results are reproducible with same seed."""
        results1 = calibrate_ci_coverage("wilson", n_sims=1000, seed=42)
        results2 = calibrate_ci_coverage("wilson", n_sims=1000, seed=42)

        # Should be identical with same seed
        assert results1["empirical_coverage"] == results2["empirical_coverage"]
        assert results1["mean_ci_width"] == results2["mean_ci_width"]

    def test_small_simulation_count(self):
        """Test with small simulation count."""
        results = calibrate_ci_coverage("wilson", n_sims=100, seed=42)

        assert results["n_simulations"] == 100
        assert 0 <= results["empirical_coverage"] <= 1
