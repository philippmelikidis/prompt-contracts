"""Tests for semantic checks."""

import pytest

from promptcontracts.core.checks.semantic import (
    contains_all_check,
    contains_any_check,
    regex_present_check,
)


def test_contains_all_check_pass():
    """Test contains_all check passing."""
    response = "The quick brown fox jumps over the lazy dog"
    spec = {"required": ["quick", "fox", "lazy"]}

    passed, message = contains_all_check(response, spec)
    assert passed is True
    assert "3" in message


def test_contains_all_check_fail():
    """Test contains_all check failing."""
    response = "The quick brown fox"
    spec = {"required": ["quick", "fox", "lazy"]}

    passed, message = contains_all_check(response, spec)
    assert passed is False
    assert "lazy" in message


def test_contains_all_case_insensitive():
    """Test contains_all with case insensitive."""
    response = "The QUICK brown FOX"
    spec = {"required": ["quick", "fox"], "case_sensitive": False}

    passed, message = contains_all_check(response, spec)
    assert passed is True


def test_contains_any_check_pass():
    """Test contains_any check passing."""
    response = "The quick brown fox"
    spec = {"options": ["quick", "slow", "fast"]}

    passed, message = contains_any_check(response, spec)
    assert passed is True
    assert "quick" in message


def test_contains_any_check_fail():
    """Test contains_any check failing."""
    response = "The brown fox"
    spec = {"options": ["quick", "slow", "fast"]}

    passed, message = contains_any_check(response, spec)
    assert passed is False


def test_regex_present_check_pass():
    """Test regex_present check passing."""
    response = "Email: alice@example.com"
    spec = {"pattern": r"[a-z]+@[a-z]+\.[a-z]+"}

    passed, message = regex_present_check(response, spec)
    assert passed is True
    assert "alice@example.com" in message


def test_regex_present_check_fail():
    """Test regex_present check failing."""
    response = "No email here"
    spec = {"pattern": r"[a-z]+@[a-z]+\.[a-z]+"}

    passed, message = regex_present_check(response, spec)
    assert passed is False


def test_regex_present_with_flags():
    """Test regex_present with flags."""
    response = "EMAIL: ALICE@EXAMPLE.COM"
    spec = {"pattern": r"email:", "flags": "i"}

    passed, message = regex_present_check(response, spec)
    assert passed is True
