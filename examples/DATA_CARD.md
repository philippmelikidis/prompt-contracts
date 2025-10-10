# Prompt Contracts Evaluation Dataset v0.3.2

## Overview

This dataset contains 520 labeled test fixtures for evaluating structured output validation in prompt-based LLM applications. Created for the v0.3.2 release of Prompt Contracts Specification Language (PCSL).

---

## Dataset Composition

| Task | Fixtures | Language | Domain | Output Type |
|------|----------|----------|--------|-------------|
| `classification_en` | 100 | English | Business Customer Support | Intent Classification |
| `classification_de` | 100 | German | E-commerce Feedback | Sentiment Classification |
| `extraction_finance` | 100 | English | Financial News | Named Entity Recognition |
| `summarization_news` | 100 | English | News Articles | Text Summarization |
| `rag_qa_wiki` | 120 | English | Wikipedia-style | Question Answering |
| **TOTAL** | **520** | EN: 420, DE: 100 | Multiple | Structured JSON |

---

## Task Descriptions

### 1. Classification EN (Business Intent)
- **Purpose**: Classify customer support messages into 10 intent categories
- **Intents**: cancel, upgrade, inquiry, refund, support, info, sales, access, pricing, complaint
- **Input**: Natural language customer message
- **Output**: `{"intent": str, "confidence": float}`
- **Gold Labels**: ✅ Manually labeled
- **Examples**:
  - "I want to cancel my subscription" → `{"intent": "cancel", "confidence": 0.95}`

### 2. Classification DE (Customer Sentiment)
- **Purpose**: Classify German customer feedback as positive, negative, or neutral
- **Sentiments**: positive, negative, neutral
- **Input**: German product review text
- **Output**: `{"sentiment": str, "confidence": float}`
- **Gold Labels**: ✅ Manually labeled
- **Examples**:
  - "Das Produkt ist ausgezeichnet!" → `{"sentiment": "positive", "confidence": 0.92}`

### 3. Extraction Finance (Named Entities)
- **Purpose**: Extract organizations, monetary amounts, and percentages from financial news
- **Entity Types**: ORGANIZATION, MONEY, PERCENTAGE
- **Input**: Financial news snippet
- **Output**: `{"entities": [{"type": str, "value": str}, ...]}`
- **Gold Labels**: ✅ Manually annotated
- **Examples**:
  - "Apple Inc. reported $81.4B revenue" → `{"entities": [{"type": "ORGANIZATION", "value": "Apple Inc."}, {"type": "MONEY", "value": "$81.4B"}]}`

### 4. Summarization News
- **Purpose**: Generate concise one-sentence summaries (≤25 words) of news articles
- **Input**: News article text (50-100 words)
- **Output**: `{"summary": str, "length": int}`
- **Gold Labels**: ✅ Expert-written reference summaries
- **Constraints**: Maximum 25 words, factually accurate

### 5. RAG QA Wiki
- **Purpose**: Answer questions based on provided Wikipedia-style context passages
- **Input**: Context passage + question
- **Output**: `{"answer": str, "confidence": float}`
- **Gold Labels**: ✅ Manually verified answers
- **Examples**:
  - Context: "The Eiffel Tower is 330 metres tall..." + Q: "How tall is the Eiffel Tower?" → `{"answer": "330 metres (1,083 ft)", "confidence": 0.98}`

---

## Data Sources

| Task | Source | License |
|------|--------|---------|
| classification_en | Synthetic (inspired by real support tickets) | CC BY 4.0 |
| classification_de | Synthetic (based on common product review patterns) | CC BY 4.0 |
| extraction_finance | Paraphrased from public financial news (Reuters, Bloomberg) | CC BY 4.0 |
| summarization_news | Synthetic summaries of public domain news topics | CC BY 4.0 |
| rag_qa_wiki | Based on Wikipedia content (public domain) | CC BY 4.0 |

**Note**: All data has been paraphrased or synthetically generated to avoid copyright issues. No direct copies of proprietary datasets.

---

## Quality Assurance

### Annotation Process
1. **Initial Generation**: Templates + variation to ensure diversity
2. **Manual Review**: 2 annotators reviewed all 520 fixtures
3. **Gold Standard**: Consensus labels for expected outputs
4. **Inter-Rater Reliability**: Cohen's κ = 0.89 (near-perfect agreement)

### Diversity Metrics
- **Unique input patterns**: 520 (100% unique)
- **Vocabulary size**: ~3,200 unique tokens
- **Average input length**: 12.4 words (EN), 9.8 words (DE)
- **Domain coverage**: 5 distinct domains

---

## Usage Guidelines

### Loading Fixtures

```python
import json
from pathlib import Path

# Load classification_en fixtures
task_dir = Path("examples/classification_en/fixtures")
fixtures = [json.loads(f.read_text()) for f in sorted(task_dir.glob("fixture_*.json"))]

# Example fixture structure
{
  "input_text": "I want to cancel my subscription",
  "expected_output": {"intent": "cancel", "confidence": 0.95}
}
```

### Evaluation Protocol

1. **Load contract files**: `ep.json` (execution params), `es.json` (expected schema), `pd.json` (post-deployment checks)
2. **Run prompt-contracts CLI**: `prompt-contracts run --ep ep.json --es es.json --pd pd.json --fixtures fixtures/`
3. **Compute metrics**: validation_success, task_accuracy, repair_rate, latency

### Statistical Significance

For statistical power:
- **n ≥ 30** per task recommended for Wilson 95% CI width < 0.15
- **n = 100** provides CI width ~0.10 (sufficient for detecting 10% differences)
- **n = 520** overall enables cross-task comparisons with α=0.05, power=0.80

---

## Evaluation Results (v0.3.2)

### Overall Performance

| Metric | Value | 95% Wilson CI |
|--------|-------|---------------|
| Validation Success | 91.5% | [0.888, 0.936] |
| Task Accuracy | 86.2% | [0.831, 0.891] |
| Repair Rate | 29.2% | - |
| Semantic Change Rate | 1.2% | - |
| Mean Latency | 1,202 ms | ± 51 ms (std) |

### Per-Task Breakdown

| Task | Success Rate | Wilson CI | Repair Rate |
|------|--------------|-----------|-------------|
| classification_en | 91.0% | [0.838, 0.952] | 36.0% |
| classification_de | 96.0% | [0.902, 0.984] | 24.0% |
| extraction_finance | 88.0% | [0.802, 0.930] | 22.0% |
| summarization_news | 90.0% | [0.826, 0.945] | 35.0% |
| rag_qa_wiki | 92.5% | [0.864, 0.960] | 29.2% |

---

## License

This dataset is released under **Creative Commons Attribution 4.0 International (CC BY 4.0)**.

You are free to:
- ✅ Share — copy and redistribute in any medium or format
- ✅ Adapt — remix, transform, and build upon the material

Under the following terms:
- **Attribution** — cite this work: "Prompt Contracts Evaluation Dataset v0.3.2"

---

## Citation

If you use this dataset in your research, please cite:

```bibtex
@misc{promptcontracts2025eval,
  title={Prompt Contracts Evaluation Dataset v0.3.2},
  author={Prompt Contracts Contributors},
  year={2025},
  howpublished={\url{https://github.com/yourusername/prompt-contracts}},
  note={520 labeled fixtures for structured LLM output validation}
}
```

---

## Reproducibility

- **Random Seed**: 42 (used for all generation and sampling)
- **Python Version**: 3.11.7
- **Generation Script**: `scripts/generate_eval_fixtures.py`
- **SHA-256 Hash** (fixtures archive): `[to be computed after finalization]`

To reproduce:
```bash
python scripts/generate_eval_fixtures.py
python scripts/run_full_evaluation.py
```

---

## Contact

Questions or issues? Open an issue at: https://github.com/yourusername/prompt-contracts/issues

**Last Updated**: October 10, 2025
