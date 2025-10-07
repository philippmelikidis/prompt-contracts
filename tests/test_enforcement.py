"""Tests for enforcement features (normalization, schema derivation, retries)."""

import pytest
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from promptcontracts.core.validator import (
    normalize_output,
    derive_json_schema_from_es,
    build_constraints_block
)
from promptcontracts.core.checks.enum_value import enum_check


def test_normalize_output_strip_fences():
    """Test stripping markdown fences."""
    raw = "```json\n{\"key\": \"value\"}\n```"
    config = {"strip_markdown_fences": True, "lowercase_fields": []}
    
    normalized, details = normalize_output(raw, config)
    
    assert normalized == "{\"key\": \"value\"}"
    assert details["stripped_fences"] is True


def test_normalize_output_lowercase_fields():
    """Test lowercasing JSONPath fields."""
    raw = '{"priority": "High", "category": "Bug"}'
    config = {
        "strip_markdown_fences": False,
        "lowercase_fields": ["$.priority"]
    }
    
    normalized, details = normalize_output(raw, config)
    
    parsed = json.loads(normalized)
    assert parsed["priority"] == "high"
    assert parsed["category"] == "Bug"  # Not lowercased
    assert "$.priority" in details["lowercased_fields"]


def test_normalize_output_combined():
    """Test stripping fences and lowercasing together."""
    raw = "```json\n{\"priority\":\"URGENT\",\"status\":\"Open\"}\n```"
    config = {
        "strip_markdown_fences": True,
        "lowercase_fields": ["$.priority", "$.status"]
    }
    
    normalized, details = normalize_output(raw, config)
    
    parsed = json.loads(normalized)
    assert parsed["priority"] == "urgent"
    assert parsed["status"] == "open"
    assert details["stripped_fences"] is True
    assert len(details["lowercased_fields"]) == 2


def test_derive_json_schema_from_es():
    """Test deriving JSON schema from ES."""
    es = {
        "pcsl": "0.1.0",
        "checks": [
            {
                "type": "pc.check.json_required",
                "fields": ["category", "priority", "reason"]
            },
            {
                "type": "pc.check.enum",
                "field": "$.priority",
                "allowed": ["low", "medium", "high"]
            }
        ]
    }
    
    schema = derive_json_schema_from_es(es)
    
    assert schema["type"] == "object"
    assert set(schema["required"]) == {"category", "priority", "reason"}
    assert "priority" in schema["properties"]
    assert schema["properties"]["priority"]["enum"] == ["low", "medium", "high"]
    assert "category" in schema["properties"]
    assert schema["properties"]["category"]["type"] == "string"


def test_build_constraints_block():
    """Test building constraints block from ES."""
    es = {
        "checks": [
            {"type": "pc.check.json_valid"},
            {"type": "pc.check.json_required", "fields": ["name", "age"]},
            {"type": "pc.check.enum", "field": "$.status", "allowed": ["active", "inactive"]},
            {"type": "pc.check.regex_absent", "pattern": "```"},
            {"type": "pc.check.token_budget", "max_out": 150}
        ]
    }
    
    constraints = build_constraints_block(es)
    
    assert "[CONSTRAINTS]" in constraints
    assert "Output MUST be strict JSON" in constraints
    assert "Required fields: name, age" in constraints
    assert "`status` MUST be exactly one of: active, inactive" in constraints
    assert "Do NOT include markdown code fences" in constraints
    assert "under 150 tokens/words" in constraints


def test_enum_check_case_insensitive():
    """Test enum check with case insensitive flag."""
    parsed = {"priority": "High"}
    check_spec = {
        "field": "$.priority",
        "allowed": ["low", "medium", "high"],
        "case_insensitive": True
    }
    
    passed, message, _ = enum_check("", check_spec, parsed_json=parsed)
    
    assert passed is True
    assert "case-insensitive" in message


def test_enum_check_case_sensitive_fail():
    """Test enum check fails with wrong case when case_sensitive."""
    parsed = {"priority": "High"}
    check_spec = {
        "field": "$.priority",
        "allowed": ["low", "medium", "high"],
        "case_insensitive": False
    }
    
    passed, message, _ = enum_check("", check_spec, parsed_json=parsed)
    
    assert passed is False
    assert "not in allowed values" in message

