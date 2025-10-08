"""Tests for output normalization utilities."""

import pytest
from promptcontracts.utils.normalization import (
    lowercase_jsonpath_fields,
    normalize_output,
    strip_code_fences,
)


class TestStripCodeFences:
    """Test markdown code fence stripping."""

    def test_strip_json_fences(self):
        """Test stripping ```json fences."""
        text = '```json\n{"key": "value"}\n```'
        result, stripped = strip_code_fences(text)
        assert result == '{"key": "value"}'
        assert stripped is True

    def test_strip_plain_fences(self):
        """Test stripping plain ``` fences."""
        text = '```\n{"key": "value"}\n```'
        result, stripped = strip_code_fences(text)
        assert result == '{"key": "value"}'
        assert stripped is True

    def test_no_fences(self):
        """Test text without fences is unchanged."""
        text = '{"key": "value"}'
        result, stripped = strip_code_fences(text)
        assert result == '{"key": "value"}'
        assert stripped is False

    def test_whitespace_handling(self):
        """Test proper whitespace handling."""
        text = '  ```json\n{"key": "value"}\n```  '
        result, stripped = strip_code_fences(text)
        assert result == '{"key": "value"}'
        assert stripped is True


class TestLowercaseJsonpathFields:
    """Test JSONPath field lowercasing."""

    def test_lowercase_single_field(self):
        """Test lowercasing a single field."""
        json_text = '{"priority": "HIGH", "status": "open"}'
        result, modified = lowercase_jsonpath_fields(json_text, ["$.priority"])
        assert '"priority": "high"' in result
        assert "$.priority" in modified

    def test_lowercase_multiple_fields(self):
        """Test lowercasing multiple fields."""
        json_text = '{"priority": "HIGH", "status": "OPEN"}'
        result, modified = lowercase_jsonpath_fields(json_text, ["$.priority", "$.status"])
        assert '"priority": "high"' in result
        assert '"status": "open"' in result
        assert len(modified) == 2

    def test_no_change_already_lowercase(self):
        """Test field already lowercase is not marked as modified."""
        json_text = '{"priority": "low"}'
        result, modified = lowercase_jsonpath_fields(json_text, ["$.priority"])
        assert '"priority": "low"' in result
        assert len(modified) == 0

    def test_invalid_json(self):
        """Test invalid JSON returns unchanged."""
        json_text = "not valid json"
        result, modified = lowercase_jsonpath_fields(json_text, ["$.priority"])
        assert result == json_text
        assert len(modified) == 0

    def test_field_without_dollar(self):
        """Test field path without $. prefix."""
        json_text = '{"priority": "HIGH"}'
        result, modified = lowercase_jsonpath_fields(json_text, ["priority"])
        assert '"priority": "high"' in result
        assert "priority" in modified

    def test_non_string_field(self):
        """Test non-string field is not modified."""
        json_text = '{"priority": 123}'
        result, modified = lowercase_jsonpath_fields(json_text, ["$.priority"])
        assert result == json_text
        assert len(modified) == 0


class TestNormalizeOutput:
    """Test complete output normalization."""

    def test_normalize_with_fences_and_lowercase(self):
        """Test normalization with both fences and lowercase."""
        raw_text = '```json\n{"priority": "HIGH", "reason": "urgent"}\n```'
        config = {"strip_markdown_fences": True, "lowercase_fields": ["$.priority"]}
        result, details = normalize_output(raw_text, config)

        assert '{"priority": "high"' in result
        assert details["stripped_fences"] is True
        assert "$.priority" in details["lowercased_fields"]

    def test_normalize_fences_only(self):
        """Test normalization with only fence stripping."""
        raw_text = '```\n{"key": "value"}\n```'
        config = {"strip_markdown_fences": True}
        result, details = normalize_output(raw_text, config)

        assert result == '{"key": "value"}'
        assert details["stripped_fences"] is True
        assert len(details["lowercased_fields"]) == 0

    def test_normalize_lowercase_only(self):
        """Test normalization with only lowercase."""
        raw_text = '{"priority": "HIGH"}'
        config = {"strip_markdown_fences": False, "lowercase_fields": ["$.priority"]}
        result, details = normalize_output(raw_text, config)

        assert '"priority": "high"' in result
        assert details["stripped_fences"] is False
        assert "$.priority" in details["lowercased_fields"]

    def test_normalize_no_changes(self):
        """Test normalization with no actual changes."""
        raw_text = '{"priority": "low"}'
        config = {"strip_markdown_fences": True, "lowercase_fields": ["$.priority"]}
        result, details = normalize_output(raw_text, config)

        assert result == raw_text
        assert details["stripped_fences"] is False
        assert len(details["lowercased_fields"]) == 0

    def test_normalize_empty_config(self):
        """Test normalization with empty config."""
        raw_text = '```json\n{"key": "VALUE"}\n```'
        config = {}
        result, details = normalize_output(raw_text, config)

        # Default is to strip fences
        assert result == '{"key": "VALUE"}'
        assert details["stripped_fences"] is True
