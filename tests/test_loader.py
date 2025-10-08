"""Tests for loader module."""

import json
import sys
from pathlib import Path

import pytest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from promptcontracts.core.loader import load_ep, load_es, load_json_or_yaml, load_pd
from promptcontracts.utils.errors import SpecValidationError


def test_load_json_or_yaml_json(tmp_path):
    """Test loading a JSON file."""
    test_file = tmp_path / "test.json"
    test_file.write_text('{"key": "value"}')

    result = load_json_or_yaml(str(test_file))
    assert result == {"key": "value"}


def test_load_json_or_yaml_yaml(tmp_path):
    """Test loading a YAML file."""
    test_file = tmp_path / "test.yaml"
    test_file.write_text("key: value")

    result = load_json_or_yaml(str(test_file))
    assert result == {"key": "value"}


def test_load_pd_valid(tmp_path):
    """Test loading a valid PD."""
    pd_data = {
        "pcsl": "0.1.0",
        "id": "test.pd",
        "io": {"channel": "text", "expects": "structured/json"},
        "prompt": "Test prompt",
    }

    test_file = tmp_path / "pd.json"
    test_file.write_text(json.dumps(pd_data))

    result = load_pd(str(test_file))
    assert result["id"] == "test.pd"


def test_load_pd_invalid_missing_field(tmp_path):
    """Test loading an invalid PD (missing required field)."""
    pd_data = {
        "pcsl": "0.1.0",
        # Missing 'id' field
        "io": {"channel": "text", "expects": "structured/json"},
        "prompt": "Test prompt",
    }

    test_file = tmp_path / "pd.json"
    test_file.write_text(json.dumps(pd_data))

    with pytest.raises(SpecValidationError, match="Prompt Definition validation failed"):
        load_pd(str(test_file))
