"""Tests for parser module."""

import pytest
from promptcontracts.core.parser import (
    ParseError,
    extract_json_field,
    json_loose,
    regex_extract,
    regex_extract_all,
    strip_markdown_fences,
)


def test_json_loose_direct():
    """Test direct JSON parsing."""
    text = '{"name": "Alice", "age": 30}'
    result = json_loose(text)
    assert result == {"name": "Alice", "age": 30}


def test_json_loose_markdown():
    """Test JSON extraction from markdown fences."""
    text = '```json\n{"name": "Bob", "age": 25}\n```'
    result = json_loose(text)
    assert result == {"name": "Bob", "age": 25}


def test_json_loose_embedded():
    """Test JSON extraction from embedded block."""
    text = 'Here is the JSON: {"name": "Charlie", "age": 35} and more text'
    result = json_loose(text)
    assert result == {"name": "Charlie", "age": 35}


def test_json_loose_with_prefix():
    """Test JSON with common prefixes."""
    text = 'JSON: {"name": "David", "age": 40}'
    result = json_loose(text)
    assert result == {"name": "David", "age": 40}


def test_json_loose_array():
    """Test JSON array extraction."""
    text = "Response: [1, 2, 3, 4, 5]"
    result = json_loose(text)
    assert result == [1, 2, 3, 4, 5]


def test_json_loose_invalid():
    """Test error on invalid JSON."""
    text = "This is not JSON at all"
    with pytest.raises(ParseError):
        json_loose(text)


def test_regex_extract():
    """Test regex extraction."""
    text = "Email: alice@example.com"
    result = regex_extract(text, r"[a-z]+@[a-z]+\.[a-z]+")
    assert result == "alice@example.com"


def test_regex_extract_group():
    """Test regex extraction with group."""
    text = "Name: Alice Smith"
    result = regex_extract(text, r"Name: (\w+)", group=1)
    assert result == "Alice"


def test_regex_extract_not_found():
    """Test regex when pattern not found."""
    text = "No match here"
    result = regex_extract(text, r"\d+")
    assert result is None


def test_regex_extract_all():
    """Test extracting all matches."""
    text = "Numbers: 123, 456, 789"
    results = regex_extract_all(text, r"\d+")
    assert results == ["123", "456", "789"]


def test_extract_json_field():
    """Test extracting nested JSON field."""
    data = {"user": {"name": "Alice", "age": 30}, "items": [{"id": 1}, {"id": 2}]}

    assert extract_json_field(data, "user.name") == "Alice"
    assert extract_json_field(data, "items.0.id") == 1
    assert extract_json_field(data, "missing", default="N/A") == "N/A"


def test_strip_markdown_fences():
    """Test stripping markdown code fences."""
    text = '```json\n{"name": "test"}\n```'
    result = strip_markdown_fences(text)
    assert result == '{"name": "test"}'

    # No fences
    text_plain = "plain text"
    result = strip_markdown_fences(text_plain)
    assert result == text_plain
