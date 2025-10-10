"""
Evaluation utilities for PCSL v0.3.2.

Provides repair analysis, baseline comparisons, and cross-dataset loaders.
"""

from .baselines import BaselineSystem, compare_systems
from .bench_loaders import load_bbh_subset, load_helm_subset
from .repair_analysis import (
    RepairEvent,
    estimate_semantic_change,
    generate_repair_sensitivity_report,
)

__all__ = [
    "RepairEvent",
    "estimate_semantic_change",
    "generate_repair_sensitivity_report",
    "BaselineSystem",
    "compare_systems",
    "load_helm_subset",
    "load_bbh_subset",
]
