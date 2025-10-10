# Classification Task Fixtures

## Description

Multi-class text classification tasks including sentiment analysis, intent detection, and topic categorization.

## Task Details

- **Task Type**: Classification
- **Output Format**: JSON with `class` field
- **Evaluation**: Exact match on class label
- **Difficulty**: Easy to Medium

## Sources

- Synthetic examples generated for evaluation purposes
- Based on common support ticket and customer feedback patterns
- Balanced across classes to avoid label bias

## Statistics

- **Total Fixtures**: 50
- **Classes**: 5 (positive, negative, neutral, urgent, question)
- **Class Distribution**:
  - positive: 10 (20%)
  - negative: 10 (20%)
  - neutral: 10 (20%)
  - urgent: 10 (20%)
  - question: 10 (20%)
- **Average Input Length**: 45 tokens
- **Labeling Agreement**: κ = 0.89 (substantial)

## Schema

```json
{
  "type": "object",
  "properties": {
    "class": {
      "type": "string",
      "enum": ["positive", "negative", "neutral", "urgent", "question"]
    },
    "confidence": {
      "type": "number",
      "minimum": 0,
      "maximum": 1
    }
  },
  "required": ["class"]
}
```

## Example

**Input**:
```
"This is great, thank you so much for the quick response!"
```

**Expected Output**:
```json
{
  "class": "positive",
  "confidence": 0.95
}
```

## License

CC BY 4.0 - See `LICENSE.txt` in this directory.
