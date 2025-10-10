"""
Compositional semantics for multi-stage contracts.

Provides variance bounds and CI aggregation for composed checks.
"""

import math


def variance_upper_bound(var1: float, var2: float) -> float:
    """
    Conservative variance upper bound for composition.

    Under independence: Var(C_total) = Var(C1) + Var(C2)
    Without independence assumption: Var(C_total) ≤ Var(C1) + Var(C2) + 2*sqrt(Var(C1)*Var(C2))

    Args:
        var1: Variance of first contract
        var2: Variance of second contract

    Returns:
        Upper bound on total variance
    """
    # Conservative bound (allows for perfect positive correlation)
    return var1 + var2 + 2 * math.sqrt(var1 * var2)


def independent_variance(var1: float, var2: float) -> float:
    """
    Variance under independence assumption.

    Args:
        var1: Variance of first contract
        var2: Variance of second contract

    Returns:
        Total variance assuming independence
    """
    return var1 + var2


def aggregate_cis_intersection(
    ci1: tuple[float, float], ci2: tuple[float, float]
) -> tuple[float, float]:
    """
    Conservative CI aggregation via intersection.

    For overall success probability when both stages must pass.

    Args:
        ci1: (lo, hi) for first stage
        ci2: (lo, hi) for second stage

    Returns:
        Intersected CI
    """
    # Conservative: take intersection (narrower interval)
    lo = max(ci1[0], ci2[0])
    hi = min(ci1[1], ci2[1])

    # Ensure valid interval
    if lo > hi:
        # No overlap - use most conservative bound
        return (min(ci1[0], ci2[0]), max(ci1[1], ci2[1]))

    return (lo, hi)


def aggregate_cis_product(
    ci1: tuple[float, float], ci2: tuple[float, float]
) -> tuple[float, float]:
    """
    Product-based CI aggregation (independence assumption).

    P(both pass) ≈ P(stage1) * P(stage2)

    Args:
        ci1: (lo, hi) for first stage
        ci2: (lo, hi) for second stage

    Returns:
        Product-based CI
    """
    lo = ci1[0] * ci2[0]
    hi = ci1[1] * ci2[1]

    return (lo, hi)


def compose_contracts_sequential(stages: list[dict]) -> dict:
    """
    Compose multiple contract stages sequentially.

    Args:
        stages: List of stage results with 'pass_rate', 'variance', 'ci'

    Returns:
        Combined contract result
    """
    if not stages:
        return {"pass_rate": 1.0, "variance": 0.0, "ci": (1.0, 1.0)}

    # Overall pass rate (assuming independence)
    overall_pass_rate = 1.0
    for stage in stages:
        overall_pass_rate *= stage["pass_rate"]

    # Variance bound
    total_variance = sum(stage["variance"] for stage in stages)

    # CI aggregation (conservative intersection)
    overall_ci = stages[0]["ci"]
    for stage in stages[1:]:
        overall_ci = aggregate_cis_intersection(overall_ci, stage["ci"])

    return {"pass_rate": overall_pass_rate, "variance": total_variance, "ci": overall_ci}
