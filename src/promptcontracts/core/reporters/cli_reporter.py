"""CLI reporter with rich formatting."""

from typing import Dict, Any
from rich.console import Console
from rich.table import Table
from rich import box


class CLIReporter:
    """Pretty CLI reporter using rich."""
    
    def __init__(self):
        self.console = Console()
    
    def report(self, results: Dict[str, Any], output_path: str = None):
        """
        Print results to CLI.
        
        Args:
            results: Results from ContractRunner
            output_path: Ignored for CLI reporter
        """
        for target_result in results.get('targets', []):
            self._report_target(target_result)
    
    def _report_target(self, target_result: Dict[str, Any]):
        """Report results for a single target."""
        target = target_result['target']
        target_type = target.get('type')
        model = target.get('model')
        
        self.console.print()
        self.console.print(f"[bold cyan]TARGET {target_type}: {model}[/bold cyan]")
        self.console.print()
        
        # Print fixture results
        for fixture_result in target_result.get('fixtures', []):
            fixture_id = fixture_result.get('fixture_id')
            latency_ms = fixture_result.get('latency_ms')
            
            self.console.print(f"[bold]Fixture:[/bold] {fixture_id} (latency: {latency_ms}ms)")
            
            # Print checks
            for check in fixture_result.get('checks', []):
                self._print_check(check)
            
            self.console.print()
        
        # Print latency checks if any
        summary = target_result.get('summary', {})
        latency_checks = summary.get('latency_checks', [])
        if latency_checks:
            self.console.print("[bold]Aggregate Checks:[/bold]")
            # Re-run to display (already computed in summary)
            # For now, just note them
            self.console.print("  (Latency budget checks evaluated across all fixtures)")
        
        # Print summary
        self._print_summary(summary)
    
    def _print_check(self, check: Dict[str, Any]):
        """Print a single check result."""
        passed = check.get('passed')
        check_type = check.get('type')
        message = check.get('message')
        
        status_symbol = "✓" if passed else "✗"
        status_text = "PASS" if passed else "FAIL"
        status_color = "green" if passed else "red"
        
        self.console.print(f"  [{status_color}]{status_symbol} {status_text}[/{status_color}] | {check_type}")
        self.console.print(f"         {message}")
    
    def _print_summary(self, summary: Dict[str, Any]):
        """Print summary."""
        total = summary.get('total_checks', 0)
        passed = summary.get('passed_checks', 0)
        status = summary.get('status', 'UNKNOWN')
        
        status_colors = {
            'GREEN': 'green',
            'YELLOW': 'yellow',
            'RED': 'red',
        }
        status_color = status_colors.get(status, 'white')
        
        self.console.print("=" * 60)
        self.console.print(f"[bold]Summary:[/bold] {passed}/{total} checks passed — status: [{status_color}]{status}[/{status_color}]")
        self.console.print("=" * 60)
        self.console.print()

