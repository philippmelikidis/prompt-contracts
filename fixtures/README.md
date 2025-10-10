# Prompt Contracts Fixtures

This directory contains labeled evaluation fixtures for PCSL v0.3.x benchmarking and reproducibility.

## Overview

All fixtures are synthetic or publicly sourced, labeled by domain experts following the protocol outlined in `docs/DATA_CARD.md`. These datasets enable reproducible evaluation of LLM prompt contracts across structural, semantic, and behavioral dimensions.

## Task Categories

### 1. Classification (`classification/`)
Multi-class text classification tasks including sentiment analysis and intent detection.

### 2. Extraction (`extraction/`)
Structured information extraction from unstructured text (contact info, entities, key-value pairs).

### 3. RAG Q&A (`rag_qa/`)
Retrieval-augmented generation question answering with context passages.

### 4. Summarization (`summarization/`)
Text summarization tasks with reference summaries for semantic validation.

### 5. Tool Calls (`tool_calls/`)
Function-calling and tool-use scenarios with expected JSON outputs.

## Structure

Each task directory contains:

```
<task>/
├── README.md          # Task description, source, and usage
├── LICENSE.txt        # CC BY 4.0 license
├── metadata.json      # Configuration (seed, version, stats)
├── fixtures.jsonl     # Fixture data (one JSON per line)
└── labels.jsonl       # Gold labels (one JSON per line)
```

## Fixture Format

**fixtures.jsonl** (one per line):
```json
{"id": "fix_001", "input": "...", "metadata": {"domain": "support", "difficulty": "easy"}}
```

**labels.jsonl** (one per line):
```json
{"id": "fix_001", "gold_output": {...}, "checks_pass": ["json_valid", "required_fields"], "task_correct": true}
```

## Reproducibility

- **Random Seed**: 42 (set in metadata.json)
- **Labeling Protocol**: See `docs/DATA_CARD.md` § Annotation Process
- **Inter-Rater Reliability**: Cohen's κ and Fleiss' κ reported per task
- **Version**: PCSL v0.3.1

## Usage

```python
from promptcontracts import ContractRunner
import json

# Load fixtures
with open("fixtures/extraction/fixtures.jsonl") as f:
    fixtures = [json.loads(line) for line in f]

# Run evaluation
runner = ContractRunner(pd_path="...", es_path="...", ep_path="...")
results = runner.run(fixtures=fixtures)
```

## License

All fixtures are released under **Creative Commons Attribution 4.0 International (CC BY 4.0)**.

See individual `LICENSE.txt` files in each task directory.

## Citation

If you use these fixtures in your research, please cite:

```bibtex
@misc{promptcontracts2025,
  title={Prompt Contracts: Specification and Enforcement for LLM Interactions},
  author={Melikidis, Philippos},
  year={2025},
  url={https://github.com/philippmelikidis/prompt-contracts}
}
```

## Contributing

To contribute new fixtures:

1. Follow the format in existing tasks
2. Include metadata.json with seed and statistics
3. Provide clear README.md with source and license
4. Run `make validate-fixtures` to verify format
5. Submit PR with Data Card updates

## Contact

For questions about fixtures or labeling protocol, open an issue at:
https://github.com/philippmelikidis/prompt-contracts/issues
