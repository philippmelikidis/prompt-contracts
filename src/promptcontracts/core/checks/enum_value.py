"""Check: Enum value validation."""

from typing import Dict, Any, Tuple
from jsonpath_ng import parse


def enum_check(response_text: str, check_spec: Dict[str, Any], parsed_json: Any = None, **kwargs) -> Tuple[bool, str, Any]:
    """
    Validate that a field (selected via JSONPath) has an allowed value.
    
    Args:
        response_text: Raw response text
        check_spec: Check configuration with 'field' (JSONPath) and 'allowed' array
        parsed_json: Pre-parsed JSON object
    
    Returns:
        (passed, message, None)
    """
    if parsed_json is None:
        return False, "Cannot check enum: response is not valid JSON", None
    
    field_path = check_spec.get('field', '$')
    allowed_values = check_spec.get('allowed', [])
    
    try:
        jsonpath_expr = parse(field_path)
        matches = jsonpath_expr.find(parsed_json)
        
        if not matches:
            return False, f"Field '{field_path}' not found in response", None
        
        # Check first match (typically there's only one)
        actual_value = matches[0].value
        
        if actual_value in allowed_values:
            return True, f"Value '{actual_value}' is in allowed values {allowed_values}", None
        else:
            return False, f"Value '{actual_value}' not in allowed values {allowed_values}", None
            
    except Exception as e:
        return False, f"Error evaluating JSONPath '{field_path}': {e}", None

