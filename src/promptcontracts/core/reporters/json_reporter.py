"""JSON reporter for machine-readable output."""

import json
from typing import Dict, Any
from pathlib import Path


class JSONReporter:
    """JSON reporter."""
    
    def report(self, results: Dict[str, Any], output_path: str = None):
        """
        Write results as JSON.
        
        Args:
            results: Results from ContractRunner
            output_path: Path to write JSON (if None, print to stdout)
        """
        json_output = json.dumps(results, indent=2)
        
        if output_path:
            Path(output_path).write_text(json_output)
            print(f"Results written to {output_path}")
        else:
            print(json_output)

