"""
Repair policy risk analysis.

Analyzes semantic vs. syntactic changes from repair transformations.
"""

from dataclasses import dataclass


@dataclass
class RepairEvent:
    """Single repair event with before/after state."""

    fixture_id: str
    type: str  # e.g., "strip_markdown_fences", "lowercase_keys"
    before: str
    after: str
    changed_fields: list[str]
    semantic_diff: bool  # Heuristic: did semantic content change?


def estimate_semantic_change(
    before: str, after: str, threshold: float = 0.95, judge_adapter=None
) -> bool:
    """
    Estimate if repair changed semantic content.

    Strategy:
    1. Heuristic: Compare JSON content ignoring formatting
    2. If ambiguous and judge_adapter provided, use LLM judge with small budget

    Args:
        before: Original output
        after: Repaired output
        threshold: Similarity threshold (default 0.95)
        judge_adapter: Optional LLM judge for ambiguous cases

    Returns:
        True if semantic content likely changed

    Example:
        >>> before = '```json\\n{"status": "ok"}\\n```'
        >>> after = '{"status": "ok"}'
        >>> estimate_semantic_change(before, after)
        False  # Only formatting changed
    """
    import json

    # Try to parse both as JSON
    try:
        before_obj = json.loads(before)
        after_obj = json.loads(after)

        # If both parse and are equal, no semantic change
        if before_obj == after_obj:
            return False

        # If keys/structure differ, likely semantic change
        if set(before_obj.keys()) != set(after_obj.keys()):
            return True

        # Check value differences
        for key in before_obj.keys():
            if before_obj[key] != after_obj[key]:
                return True

        return False

    except (json.JSONDecodeError, AttributeError):
        # If JSON parsing fails, fall back to string similarity
        if judge_adapter is not None:
            # Use judge for ambiguous cases
            prompt = f"""Compare these two outputs and determine if they are semantically equivalent.
Only formatting/syntax differs = EQUIVALENT
Content/meaning differs = DIFFERENT

Output 1: {before}
Output 2: {after}

Answer with VERDICT: EQUIVALENT or VERDICT: DIFFERENT"""

            result = judge_adapter.judge(prompt, budget={"max_tokens": 50})
            return "DIFFERENT" in result.get("explanation", "")

        # Simple heuristic: normalized string distance
        before_norm = before.lower().strip()
        after_norm = after.lower().strip()

        # Levenshtein-like approximation
        similarity = 1.0 - (
            abs(len(before_norm) - len(after_norm)) / max(len(before_norm), len(after_norm))
        )

        return similarity < threshold


def analyze_repair_events(
    events: list[RepairEvent],
) -> dict:
    """
    Analyze a collection of repair events.

    Args:
        events: List of RepairEvent instances

    Returns:
        Dictionary with analysis results
    """
    if not events:
        return {
            "total_repairs": 0,
            "semantic_changes": 0,
            "semantic_change_rate": 0.0,
            "repair_types": {},
        }

    total = len(events)
    semantic_changes = sum(1 for e in events if e.semantic_diff)

    repair_types = {}
    for event in events:
        repair_types[event.type] = repair_types.get(event.type, 0) + 1

    return {
        "total_repairs": total,
        "semantic_changes": semantic_changes,
        "semantic_change_rate": semantic_changes / total if total > 0 else 0.0,
        "repair_types": repair_types,
        "most_common_repair": (
            max(repair_types.items(), key=lambda x: x[1])[0] if repair_types else None
        ),
    }


def repair_sensitivity_table(
    results_off: dict, results_syntactic: dict, results_full: dict
) -> dict:
    """
    Generate sensitivity table comparing repair policies.

    Args:
        results_off: Results with repair disabled
        results_syntactic: Results with syntactic-only repair
        results_full: Results with full repair

    Returns:
        Comparison table as dict
    """
    return {
        "off": {
            "validation_success": results_off.get("validation_success", 0.0),
            "task_accuracy": results_off.get("task_accuracy", 0.0),
            "repair_rate": 0.0,
        },
        "syntactic": {
            "validation_success": results_syntactic.get("validation_success", 0.0),
            "task_accuracy": results_syntactic.get("task_accuracy", 0.0),
            "repair_rate": results_syntactic.get("repair_rate", 0.0),
        },
        "full": {
            "validation_success": results_full.get("validation_success", 0.0),
            "task_accuracy": results_full.get("task_accuracy", 0.0),
            "repair_rate": results_full.get("repair_rate", 0.0),
        },
        "delta_off_to_full": results_full.get("validation_success", 0.0)
        - results_off.get("validation_success", 0.0),
    }
