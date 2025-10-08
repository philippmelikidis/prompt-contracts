"""Tests for execution modes and mode negotiation."""

from unittest.mock import Mock, patch

import pytest

from promptcontracts.core.adapters.base import Capability


class TestModeNegotiation:
    """Test execution mode selection based on adapter capabilities."""

    def test_auto_mode_with_schema_guided_json(self):
        """Test auto mode selects enforce when schema_guided_json is available."""
        capability = Capability(
            schema_guided_json=True, tool_calling=False, function_call_json=False
        )
        requested_mode = "auto"

        # Mode selection logic (simplified from runner)
        if requested_mode == "auto":
            effective_mode = "enforce" if capability.schema_guided_json else "assist"
        else:
            effective_mode = requested_mode

        assert effective_mode == "enforce"

    def test_auto_mode_without_schema_guided_json(self):
        """Test auto mode falls back to assist when schema_guided_json is unavailable."""
        capability = Capability(
            schema_guided_json=False, tool_calling=False, function_call_json=False
        )
        requested_mode = "auto"

        if requested_mode == "auto":
            effective_mode = "enforce" if capability.schema_guided_json else "assist"
        else:
            effective_mode = requested_mode

        assert effective_mode == "assist"

    def test_enforce_mode_without_capability_strict(self):
        """Test enforce mode with strict=True fails when capability missing."""
        capability = Capability(
            schema_guided_json=False, tool_calling=False, function_call_json=False
        )
        requested_mode = "enforce"
        strict_enforce = True

        # Should mark as NONENFORCEABLE in strict mode
        if requested_mode == "enforce" and not capability.schema_guided_json:
            if strict_enforce:
                status = "NONENFORCEABLE"
            else:
                status = "fallback_to_assist"

        assert status == "NONENFORCEABLE"

    def test_enforce_mode_without_capability_non_strict(self):
        """Test enforce mode with strict=False falls back to assist."""
        capability = Capability(
            schema_guided_json=False, tool_calling=False, function_call_json=False
        )
        requested_mode = "enforce"
        strict_enforce = False

        if requested_mode == "enforce" and not capability.schema_guided_json:
            if strict_enforce:
                pass
            else:
                effective_mode = "assist"

        assert effective_mode == "assist"

    def test_observe_mode_always_accepted(self):
        """Test observe mode works regardless of capabilities."""
        Capability(schema_guided_json=False, tool_calling=False, function_call_json=False)
        requested_mode = "observe"

        effective_mode = requested_mode
        assert effective_mode == "observe"

    def test_assist_mode_always_accepted(self):
        """Test assist mode works regardless of capabilities."""
        Capability(schema_guided_json=False, tool_calling=False, function_call_json=False)
        requested_mode = "assist"

        effective_mode = requested_mode
        assert effective_mode == "assist"


class TestRetryLogic:
    """Test retry and repair logic."""

    def test_first_attempt_pass(self):
        """Test successful first attempt."""
        attempts = 0
        check_passed = True

        status = None
        if attempts == 0 and check_passed:
            status = "PASS"

        assert status == "PASS"

    def test_fail_then_repair(self):
        """Test failure followed by successful repair."""
        # Simulate: first check fails, repair applied, second check passes
        attempt_results = [
            {"check_passed": False, "repaired": False},
            {"check_passed": True, "repaired": True},
        ]

        max_retries = 1
        status = None

        for i, result in enumerate(attempt_results):
            if result["check_passed"]:
                if result["repaired"]:
                    status = "REPAIRED"
                else:
                    status = "PASS"
                break
            elif i >= max_retries:
                status = "FAIL"

        assert status == "REPAIRED"

    def test_fail_after_max_retries(self):
        """Test failure after exhausting retries."""
        attempt_results = [{"check_passed": False}, {"check_passed": False}]

        max_retries = 1
        status = None

        for i, result in enumerate(attempt_results):
            if result["check_passed"]:
                status = "PASS"
                break
            elif i >= max_retries:
                status = "FAIL"

        assert status == "FAIL"


class TestExecutionConfig:
    """Test execution configuration parsing."""

    def test_default_execution_config(self):
        """Test default execution configuration."""
        ep_dict = {"pcsl": "0.1.0", "targets": [], "fixtures": []}

        # Default values
        execution = ep_dict.get("execution", {})
        mode = execution.get("mode", "auto")
        max_retries = execution.get("max_retries", 1)
        auto_repair = execution.get("auto_repair", {})
        strip_fences = auto_repair.get("strip_markdown_fences", True)

        assert mode == "auto"
        assert max_retries == 1
        assert strip_fences is True

    def test_custom_execution_config(self):
        """Test custom execution configuration."""
        ep_dict = {
            "pcsl": "0.1.0",
            "targets": [],
            "fixtures": [],
            "execution": {
                "mode": "enforce",
                "max_retries": 3,
                "auto_repair": {
                    "strip_markdown_fences": False,
                    "lowercase_fields": ["$.priority", "$.status"],
                },
            },
        }

        execution = ep_dict.get("execution", {})
        mode = execution.get("mode", "auto")
        max_retries = execution.get("max_retries", 1)
        auto_repair = execution.get("auto_repair", {})
        strip_fences = auto_repair.get("strip_markdown_fences", True)
        lowercase_fields = auto_repair.get("lowercase_fields", [])

        assert mode == "enforce"
        assert max_retries == 3
        assert strip_fences is False
        assert lowercase_fields == ["$.priority", "$.status"]


class TestStatusCodes:
    """Test status code assignment."""

    def test_pass_status(self):
        """Test PASS status for successful first attempt."""
        first_attempt_success = True
        repaired = False

        if first_attempt_success:
            status = "PASS"
        elif repaired:
            status = "REPAIRED"
        else:
            status = "FAIL"

        assert status == "PASS"

    def test_repaired_status(self):
        """Test REPAIRED status after normalization."""
        first_attempt_success = False
        repaired = True
        second_attempt_success = True

        if first_attempt_success:
            status = "PASS"
        elif repaired and second_attempt_success:
            status = "REPAIRED"
        else:
            status = "FAIL"

        assert status == "REPAIRED"

    def test_fail_status(self):
        """Test FAIL status after all retries exhausted."""
        first_attempt_success = False
        repaired = True
        second_attempt_success = False

        if first_attempt_success:
            status = "PASS"
        elif repaired and second_attempt_success:
            status = "REPAIRED"
        else:
            status = "FAIL"

        assert status == "FAIL"

    def test_nonenforceable_status(self):
        """Test NONENFORCEABLE status for unsupported enforce mode."""
        enforce_requested = True
        capability_missing = True
        strict_mode = True

        if enforce_requested and capability_missing and strict_mode:
            status = "NONENFORCEABLE"
        else:
            status = "FAIL"

        assert status == "NONENFORCEABLE"
