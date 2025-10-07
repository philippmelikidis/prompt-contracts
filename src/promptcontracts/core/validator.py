"""
Validator: Check registry and execution.
"""

from typing import Dict, Any, Callable, Tuple, List
from .checks import (
    json_valid_check,
    json_required_check,
    enum_check,
    regex_absent_check,
    token_budget_check,
    latency_budget_check,
)


class CheckRegistry:
    """Registry for check types."""
    
    def __init__(self):
        self._checks: Dict[str, Callable] = {}
        self._register_builtin_checks()
    
    def _register_builtin_checks(self):
        """Register all built-in check types."""
        self.register('pc.check.json_valid', json_valid_check)
        self.register('pc.check.json_required', json_required_check)
        self.register('pc.check.enum', enum_check)
        self.register('pc.check.regex_absent', regex_absent_check)
        self.register('pc.check.token_budget', token_budget_check)
        self.register('pc.check.latency_budget', latency_budget_check)
    
    def register(self, check_type: str, check_func: Callable):
        """Register a check function."""
        self._checks[check_type] = check_func
    
    def get(self, check_type: str) -> Callable:
        """Get a check function by type."""
        if check_type not in self._checks:
            raise ValueError(f"Unknown check type: {check_type}")
        return self._checks[check_type]
    
    def has(self, check_type: str) -> bool:
        """Check if a check type is registered."""
        return check_type in self._checks


class Validator:
    """Execute checks against responses."""
    
    def __init__(self, registry: CheckRegistry = None):
        self.registry = registry or CheckRegistry()
    
    def run_check(
        self,
        check_spec: Dict[str, Any],
        response_text: str,
        parsed_json: Any = None,
        all_latencies: List[int] = None,
    ) -> Dict[str, Any]:
        """
        Run a single check.
        
        Returns:
            {
                'type': str,
                'passed': bool,
                'message': str,
                'data': Any (optional additional data)
            }
        """
        check_type = check_spec.get('type', '')
        
        if not self.registry.has(check_type):
            return {
                'type': check_type,
                'passed': False,
                'message': f"Unknown check type: {check_type}",
                'data': None
            }
        
        check_func = self.registry.get(check_type)
        
        try:
            passed, message, data = check_func(
                response_text=response_text,
                check_spec=check_spec,
                parsed_json=parsed_json,
                all_latencies=all_latencies,
            )
            
            return {
                'type': check_type,
                'passed': passed,
                'message': message,
                'data': data
            }
        except Exception as e:
            return {
                'type': check_type,
                'passed': False,
                'message': f"Check execution failed: {e}",
                'data': None
            }
    
    def run_checks(
        self,
        check_specs: List[Dict[str, Any]],
        response_text: str,
        parsed_json: Any = None,
        all_latencies: List[int] = None,
    ) -> List[Dict[str, Any]]:
        """Run all checks and return results."""
        results = []
        
        for check_spec in check_specs:
            result = self.run_check(
                check_spec=check_spec,
                response_text=response_text,
                parsed_json=parsed_json,
                all_latencies=all_latencies,
            )
            results.append(result)
        
        return results

