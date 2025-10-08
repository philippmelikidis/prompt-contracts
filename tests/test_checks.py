"""Tests for check modules."""

import sys
from pathlib import Path

import pytest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from promptcontracts.core.checks.enum_value import enum_check
from promptcontracts.core.checks.json_required import json_required_check
from promptcontracts.core.checks.json_valid import json_valid_check


def test_json_valid_check_pass():
    """Test json_valid check with valid JSON."""
    response = '{"key": "value"}'
    passed, message, data = json_valid_check(response, {})

    assert passed is True
    assert data == {"key": "value"}


def test_json_valid_check_fail():
    """Test json_valid check with invalid JSON."""
    response = "not json"
    passed, message, data = json_valid_check(response, {})

    assert passed is False
    assert data is None


def test_json_required_check_pass():
    """Test json_required check with all fields present."""
    response = '{"name": "test", "age": 30}'
    parsed = {"name": "test", "age": 30}
    check_spec = {"fields": ["name", "age"]}

    passed, message, data = json_required_check(response, check_spec, parsed_json=parsed)

    assert passed is True


def test_json_required_check_fail():
    """Test json_required check with missing fields."""
    response = '{"name": "test"}'
    parsed = {"name": "test"}
    check_spec = {"fields": ["name", "age"]}

    passed, message, data = json_required_check(response, check_spec, parsed_json=parsed)

    assert passed is False
    assert "age" in message


def test_enum_check_pass():
    """Test enum check with allowed value."""
    response = '{"priority": "high"}'
    parsed = {"priority": "high"}
    check_spec = {"field": "$.priority", "allowed": ["low", "medium", "high"]}

    passed, message, data = enum_check(response, check_spec, parsed_json=parsed)

    assert passed is True


def test_enum_check_fail():
    """Test enum check with disallowed value."""
    response = '{"priority": "urgent"}'
    parsed = {"priority": "urgent"}
    check_spec = {"field": "$.priority", "allowed": ["low", "medium", "high"]}

    passed, message, data = enum_check(response, check_spec, parsed_json=parsed)

    assert passed is False
