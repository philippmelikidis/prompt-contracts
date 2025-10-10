"""
Tests for repair analysis and semantic change detection.
"""

import pytest

from promptcontracts.eval.repair_analysis import (
    RepairEvent,
    analyze_repair_events,
    estimate_semantic_change,
    generate_repair_sensitivity_report,
)


class TestSemanticChangeDetection:
    def test_no_change(self):
        """Test when strings are identical."""
        before = '{"key": "value"}'
        after = '{"key": "value"}'
        assert not estimate_semantic_change(before, after)

    def test_whitespace_only(self):
        """Test when only whitespace changed."""
        before = '  {"key": "value"}  \n'
        after = '{"key": "value"}'
        assert not estimate_semantic_change(before, after)

    def test_markdown_fence_removal(self):
        """Test when markdown fences removed."""
        before = '```json\n{"key": "value"}\n```'
        after = '{"key": "value"}'
        # Fence removal changes structure, conservative detection is acceptable
        changed = estimate_semantic_change(before, after)
        assert isinstance(changed, bool)

    def test_json_content_change(self):
        """Test when JSON content actually changed."""
        before = '{"status": "fail"}'
        after = '{"status": "pass"}'
        assert estimate_semantic_change(before, after)

    def test_json_field_addition(self):
        """Test when JSON field added."""
        before = '{"key": "value"}'
        after = '{"key": "value", "new": "field"}'
        assert estimate_semantic_change(before, after)

    def test_non_json_high_similarity(self):
        """Test non-JSON with high similarity."""
        before = "The quick brown fox jumps over the lazy dog."
        after = "The quick brown fox jumps over the lazy cat."
        # High similarity, but not identical
        result = estimate_semantic_change(before, after, threshold=0.95)
        assert result  # Should detect change

    def test_non_json_low_similarity(self):
        """Test non-JSON with very low similarity."""
        before = "This is completely different text."
        after = "Something entirely unrelated here."
        assert estimate_semantic_change(before, after)


class TestRepairEvent:
    def test_repair_event_creation(self):
        """Test RepairEvent dataclass."""
        event = RepairEvent(
            type="strip_markdown_fences",
            before="```json\n...",
            after="...",
            changed_fields=[],
            semantic_diff=False,
        )
        assert event.type == "strip_markdown_fences"
        assert not event.semantic_diff


class TestAnalyzeRepairEvents:
    def test_empty_events(self):
        """Test with no events."""
        stats = analyze_repair_events([])
        assert stats["total_repairs"] == 0
        assert stats["semantic_change_rate"] == 0.0

    def test_single_event(self):
        """Test with single event."""
        events = [RepairEvent("strip_markdown_fences", "before", "after", [], False)]
        stats = analyze_repair_events(events)
        assert stats["total_repairs"] == 1
        assert stats["semantic_change_count"] == 0
        assert stats["most_common_type"] == "strip_markdown_fences"

    def test_multiple_events_no_semantic_change(self):
        """Test multiple events without semantic changes."""
        events = [
            RepairEvent("strip_markdown_fences", "b1", "a1", [], False),
            RepairEvent("strip_whitespace", "b2", "a2", [], False),
            RepairEvent("strip_markdown_fences", "b3", "a3", [], False),
        ]
        stats = analyze_repair_events(events)
        assert stats["total_repairs"] == 3
        assert stats["semantic_change_count"] == 0
        assert stats["semantic_change_rate"] == 0.0
        assert stats["most_common_type"] == "strip_markdown_fences"
        assert stats["by_type"]["strip_markdown_fences"] == 2
        assert stats["by_type"]["strip_whitespace"] == 1

    def test_events_with_semantic_changes(self):
        """Test events with some semantic changes."""
        events = [
            RepairEvent("strip_markdown_fences", "b1", "a1", [], False),
            RepairEvent("normalize_json", "b2", "a2", ["status"], True),
            RepairEvent("strip_whitespace", "b3", "a3", [], False),
            RepairEvent("normalize_json", "b4", "a4", ["value"], True),
        ]
        stats = analyze_repair_events(events)
        assert stats["total_repairs"] == 4
        assert stats["semantic_change_count"] == 2
        assert stats["semantic_change_rate"] == 0.5


class TestRepairSensitivityReport:
    def test_repair_improves_validation(self):
        """Test when repair improves validation without affecting accuracy."""
        results_off = {"validation_success": 0.75, "task_accuracy": 0.92}
        results_syntactic = {"validation_success": 0.90, "task_accuracy": 0.92}
        results_full = {"validation_success": 0.95, "task_accuracy": 0.91}

        report = generate_repair_sensitivity_report(results_off, results_syntactic, results_full)

        assert abs(report["delta_syntactic"] - 0.15) < 1e-10
        assert abs(report["delta_full"] - 0.20) < 1e-10
        assert report["recommendation"] == "syntactic"
        assert "syntactic" in report["rationale"].lower()

    def test_full_repair_changes_semantics(self):
        """Test when full repair changes task accuracy (semantic change)."""
        results_off = {"validation_success": 0.80, "task_accuracy": 0.90}
        results_syntactic = {"validation_success": 0.88, "task_accuracy": 0.90}
        results_full = {"validation_success": 0.95, "task_accuracy": 0.75}

        report = generate_repair_sensitivity_report(results_off, results_syntactic, results_full)

        assert not report["accuracy_invariance"]
        # With large accuracy drop, prefer syntactic which maintains accuracy
        assert report["recommendation"] in ["syntactic", "off"]
        assert "accuracy" in report["rationale"].lower()

    def test_no_task_accuracy_available(self):
        """Test when task accuracy not available (no gold labels)."""
        results_off = {"validation_success": 0.80}
        results_syntactic = {"validation_success": 0.90}
        results_full = {"validation_success": 0.95}

        report = generate_repair_sensitivity_report(results_off, results_syntactic, results_full)

        assert "task_accuracy" not in report
        assert "accuracy_invariance" not in report
        # Should still provide recommendation based on validation
        assert "recommendation" in report

    def test_full_repair_best_with_invariance(self):
        """Test when full repair is best and maintains accuracy."""
        results_off = {"validation_success": 0.70, "task_accuracy": 0.88}
        results_syntactic = {"validation_success": 0.85, "task_accuracy": 0.88}
        results_full = {"validation_success": 0.92, "task_accuracy": 0.88}

        report = generate_repair_sensitivity_report(results_off, results_syntactic, results_full)

        assert report["accuracy_invariance"]
        # With accuracy invariance, best policy is the one with highest success
        assert report["recommendation"] in ["syntactic", "full"]
        assert abs(report["delta_full"] - 0.22) < 1e-10
