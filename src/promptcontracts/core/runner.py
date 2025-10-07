"""
Main runner: orchestrate contract execution.
"""

from typing import Dict, Any, List
from .validator import Validator, CheckRegistry
from .adapters import OpenAIAdapter, OllamaAdapter


class ContractRunner:
    """Execute PCSL contracts."""
    
    def __init__(self, pd: Dict[str, Any], es: Dict[str, Any], ep: Dict[str, Any]):
        """
        Initialize runner with artefacts.
        
        Args:
            pd: Prompt Definition
            es: Expectation Suite
            ep: Evaluation Profile
        """
        self.pd = pd
        self.es = es
        self.ep = ep
        self.validator = Validator(CheckRegistry())
    
    def _create_adapter(self, target: Dict[str, Any]):
        """Create an adapter for a target."""
        target_type = target.get('type')
        model = target.get('model')
        params = target.get('params', {})
        
        if target_type == 'openai':
            return OpenAIAdapter(model, params)
        elif target_type == 'ollama':
            return OllamaAdapter(model, params)
        else:
            raise ValueError(f"Unknown target type: {target_type}")
    
    def _build_prompt(self, fixture: Dict[str, Any]) -> str:
        """Build final prompt by combining PD prompt + fixture input."""
        base_prompt = self.pd.get('prompt', '')
        fixture_input = fixture.get('input', '')
        
        # Simple concatenation with newline separator
        return f"{base_prompt}\n\n{fixture_input}"
    
    def run(self) -> Dict[str, Any]:
        """
        Execute the contract and return results.
        
        Returns:
            {
                'targets': [
                    {
                        'target': {...},
                        'fixtures': [
                            {
                                'fixture_id': str,
                                'response_text': str,
                                'latency_ms': int,
                                'checks': [...]
                            }
                        ],
                        'summary': {...}
                    }
                ]
            }
        """
        targets = self.ep.get('targets', [])
        fixtures = self.ep.get('fixtures', [])
        checks = self.es.get('checks', [])
        tolerances = self.ep.get('tolerances', {})
        
        results = {
            'targets': []
        }
        
        for target in targets:
            adapter = self._create_adapter(target)
            
            target_result = {
                'target': target,
                'fixtures': [],
                'summary': {}
            }
            
            all_latencies = []
            all_check_results = []
            
            # Run each fixture
            for fixture in fixtures:
                prompt = self._build_prompt(fixture)
                
                # Generate response
                response_text, latency_ms = adapter.generate(prompt)
                all_latencies.append(latency_ms)
                
                # Parse JSON if expected
                parsed_json = None
                if self.pd.get('io', {}).get('expects') == 'structured/json':
                    import json
                    try:
                        parsed_json = json.loads(response_text)
                    except json.JSONDecodeError:
                        pass
                
                # Run checks (except latency_budget which needs all latencies)
                fixture_check_results = []
                for check in checks:
                    if check.get('type') == 'pc.check.latency_budget':
                        continue  # Skip latency checks for now
                    
                    result = self.validator.run_check(
                        check_spec=check,
                        response_text=response_text,
                        parsed_json=parsed_json,
                    )
                    fixture_check_results.append(result)
                    all_check_results.append(result)
                
                target_result['fixtures'].append({
                    'fixture_id': fixture.get('id'),
                    'response_text': response_text,
                    'latency_ms': latency_ms,
                    'checks': fixture_check_results
                })
            
            # Now run latency budget checks with all latencies
            latency_checks = [c for c in checks if c.get('type') == 'pc.check.latency_budget']
            for check in latency_checks:
                result = self.validator.run_check(
                    check_spec=check,
                    response_text='',  # Not needed for latency check
                    all_latencies=all_latencies,
                )
                all_check_results.append(result)
            
            # Calculate summary
            total_checks = len(all_check_results)
            passed_checks = sum(1 for r in all_check_results if r['passed'])
            pass_rate = passed_checks / total_checks if total_checks > 0 else 0
            
            # Determine status based on tolerances
            status = 'GREEN'
            for check_result in all_check_results:
                if not check_result['passed']:
                    check_type = check_result['type']
                    tolerance = tolerances.get(check_type, {})
                    max_fail_rate = tolerance.get('max_fail_rate', 0.0)
                    
                    # Simple per-check failure (more sophisticated would aggregate across fixtures)
                    if max_fail_rate == 0.0:
                        status = 'RED'
                        break
                    else:
                        status = 'YELLOW'
            
            target_result['summary'] = {
                'total_checks': total_checks,
                'passed_checks': passed_checks,
                'pass_rate': pass_rate,
                'status': status,
                'latency_checks': latency_checks
            }
            
            results['targets'].append(target_result)
        
        return results

