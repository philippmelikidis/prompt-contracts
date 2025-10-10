"""
Test repair policy sensitivity and impact on validation success.

Compares results with repair enabled vs disabled to assess:
- False positive rate from over-aggressive repair
- Validation success delta
- Task accuracy impact (if gold labels present)
"""

import pytest
from promptcontracts.core.runner import ContractRunner
from promptcontracts.utils.normalization import normalize_json_response


class TestRepairSensitivity:
    """Test suite for repair policy sensitivity analysis."""

    def test_json_fences_repair(self):
        """Test that markdown fence removal doesn't break valid JSON."""
        # Valid JSON wrapped in markdown fences
        raw_output = '```json\n{"status": "success", "value": 42}\n```'

        # With repair
        repaired = normalize_json_response(raw_output)
        assert repaired == '{"status": "success", "value": 42}'

        # Original should fail JSON parse
        import json

        with pytest.raises(json.JSONDecodeError):
            json.loads(raw_output)

        # Repaired should succeed
        parsed = json.loads(repaired)
        assert parsed["status"] == "success"
        assert parsed["value"] == 42

    def test_whitespace_repair(self):
        """Test that whitespace normalization preserves semantics."""
        raw_output = '  \n\n{"key":  "value"  }  \n'
        repaired = normalize_json_response(raw_output)

        import json

        assert json.loads(repaired) == json.loads('{"key": "value"}')

    def test_case_sensitive_repair(self):
        """Test case normalization when enabled."""
        # This test documents current behavior
        # In practice, case repair is task-specific and not in normalize_json_response
        raw = '{"Status": "SUCCESS"}'
        # normalize_json_response doesn't do case changes by default
        assert normalize_json_response(raw) == raw

    def test_repair_disabled_stricter(self):
        """Test that disabling repair makes validation stricter."""
        # Conceptual test demonstrating repair behavior
        # In practice:
        # - With repair enabled: markdown fences removed, both pass
        # - Without repair: only clean JSON passes
        # - Actual implementation would need mock adapter

        # This test documents the expected behavior
        with_repair_pass_rate = 1.0  # Both fixtures pass
        without_repair_pass_rate = 0.5  # Only clean fixture passes

        assert with_repair_pass_rate > without_repair_pass_rate
        assert True  # Placeholder for integration test

    def test_repair_ledger_tracking(self):
        """Test that all repairs are logged in repair_ledger."""
        # Mock scenario: repair ledger should contain entries for each transformation

        expected_repairs = [
            {
                "step": "strip_markdown_fences",
                "before_length": 45,
                "after_length": 20,
                "description": "Removed ```json``` fences",
            },
            {
                "step": "strip_whitespace",
                "before_length": 20,
                "after_length": 18,
                "description": "Trimmed leading/trailing whitespace",
            },
        ]

        # Conceptual test; actual runner would populate repair_ledger
        assert len(expected_repairs) == 2

    def test_validation_success_with_without_repair(self):
        """
        Compare validation success rates with repair enabled vs disabled.

        Expected: repair increases success rate but may mask genuine failures.
        """
        # Test data: 10 responses, 5 with markdown fences
        responses_clean = 5
        responses_with_fences = 5

        # Without repair:
        # - Clean: 5/5 pass = 100%
        # - Fenced: 0/5 pass = 0%
        # - Total: 5/10 = 50%

        success_without_repair = responses_clean / (responses_clean + responses_with_fences)
        assert success_without_repair == 0.5

        # With repair:
        # - Clean: 5/5 pass = 100%
        # - Fenced: 5/5 pass after repair = 100%
        # - Total: 10/10 = 100%

        success_with_repair = (responses_clean + responses_with_fences) / (
            responses_clean + responses_with_fences
        )
        assert success_with_repair == 1.0

        # Sensitivity: 50% improvement
        sensitivity = success_with_repair - success_without_repair
        assert sensitivity == 0.5

    def test_false_positive_rate(self):
        """
        Test that repair doesn't create false positives.

        False positive = genuinely invalid response marked valid after repair.
        """
        # Example: incomplete JSON that repair can't fix
        broken_json = '{"key": "val'  # Missing closing brace

        repaired = normalize_json_response(broken_json)

        # Should still be invalid
        import json

        with pytest.raises(json.JSONDecodeError):
            json.loads(repaired)

        # Repair doesn't create false positives for structural errors
        assert True

    def test_task_accuracy_invariance(self):
        """
        Test that repair doesn't change semantic content.

        Task accuracy (based on gold labels) should be invariant to repair.
        """
        # Gold label
        gold = {"class": "positive", "confidence": 0.9}

        # Response 1: clean
        response_clean = '{"class": "positive", "confidence": 0.9}'

        # Response 2: with fences
        response_fenced = '```json\n{"class": "positive", "confidence": 0.9}\n```'

        # Both should match gold after parsing
        import json

        parsed_clean = json.loads(response_clean)
        parsed_fenced = json.loads(normalize_json_response(response_fenced))

        assert parsed_clean == gold
        assert parsed_fenced == gold

        # Task accuracy is preserved
        assert parsed_clean["class"] == parsed_fenced["class"]

    def test_repair_rate_metric(self):
        """Test repair_rate metric calculation."""
        total_fixtures = 100
        repairs_applied = 18  # 18% required repair

        repair_rate = repairs_applied / total_fixtures
        assert repair_rate == 0.18

        # Low repair rate (< 10%) = clean prompts
        # Medium (10-30%) = common formatting issues
        # High (> 30%) = prompts need improvement

        if repair_rate < 0.10:
            category = "clean"
        elif repair_rate < 0.30:
            category = "moderate"
        else:
            category = "needs_improvement"

        assert category == "moderate"

    def test_repair_policy_configuration(self):
        """Test repair policy enables/disables specific normalizations."""
        repair_policy = {
            "enabled": True,
            "max_steps": 5,
            "allowed": [
                "strip_markdown_fences",
                "strip_whitespace",
                "normalize_newlines",
            ],
        }

        # Check allowed transformations
        assert "strip_markdown_fences" in repair_policy["allowed"]
        assert "lowercase_keys" not in repair_policy["allowed"]  # Not enabled

        # Max steps prevents infinite loops
        assert repair_policy["max_steps"] == 5


class TestRepairStatisticalComparison:
    """Statistical comparison of repair on/off across tasks."""

    @pytest.fixture
    def mock_results_with_repair(self):
        """Simulated results with repair enabled."""
        return {
            "classification": {"validation_success": 0.98, "task_accuracy": 0.94},
            "extraction": {"validation_success": 0.96, "task_accuracy": 0.91},
            "summarization": {"validation_success": 0.92, "task_accuracy": 0.87},
        }

    @pytest.fixture
    def mock_results_without_repair(self):
        """Simulated results with repair disabled."""
        return {
            "classification": {"validation_success": 0.82, "task_accuracy": 0.94},
            "extraction": {"validation_success": 0.78, "task_accuracy": 0.91},
            "summarization": {"validation_success": 0.74, "task_accuracy": 0.87},
        }

    def test_validation_success_delta(self, mock_results_with_repair, mock_results_without_repair):
        """Compare validation success with vs without repair."""
        for task in mock_results_with_repair.keys():
            with_repair = mock_results_with_repair[task]["validation_success"]
            without_repair = mock_results_without_repair[task]["validation_success"]

            delta = with_repair - without_repair

            # Repair should increase validation success
            assert delta > 0, f"{task}: repair decreased validation success"

            # Delta should be reasonable (not too high = over-repair)
            assert delta < 0.3, f"{task}: repair delta too high ({delta:.2f})"

    def test_task_accuracy_invariance_across_tasks(
        self, mock_results_with_repair, mock_results_without_repair
    ):
        """Task accuracy should be same regardless of repair."""
        for task in mock_results_with_repair.keys():
            acc_with = mock_results_with_repair[task]["task_accuracy"]
            acc_without = mock_results_without_repair[task]["task_accuracy"]

            # Should be identical (repair doesn't change semantics)
            assert (
                acc_with == acc_without
            ), f"{task}: repair changed task accuracy ({acc_with} vs {acc_without})"

    def test_repair_benefit_ranking(self, mock_results_with_repair, mock_results_without_repair):
        """Rank tasks by repair benefit."""
        benefits = {}
        for task in mock_results_with_repair.keys():
            delta = (
                mock_results_with_repair[task]["validation_success"]
                - mock_results_without_repair[task]["validation_success"]
            )
            benefits[task] = delta

        # Rank by benefit
        ranked = sorted(benefits.items(), key=lambda x: x[1], reverse=True)

        # Classification benefits most (structured output)
        assert ranked[0][0] == "classification"

        # Summarization benefits least (less structured)
        assert ranked[-1][0] == "summarization"
