# Compliance Mapping for prompt-contracts v0.3.0

## Overview

This document maps prompt-contracts' PCSL (Prompt Contract Specification Language) to established software testing standards and AI regulations. This demonstrates how prompt-contracts facilitates compliance with international standards and regulatory requirements.

## ISO/IEC/IEEE 29119: Software Testing Standards

### 29119-1: Concepts and Definitions

| PCSL Component | ISO 29119-1 Concept | Mapping |
|----------------|---------------------|---------|
| Prompt Definition (PD) | Test Item | The prompt is the system under test |
| Expectation Suite (ES) | Test Conditions | Checks define what must be validated |
| Evaluation Profile (EP) | Test Case | Fixtures + targets define test execution |
| Execution Mode | Test Level | observe/assist/enforce map to test rigor |
| Fixture | Test Data | Input data for test execution |

### 29119-2: Test Processes

| ISO Process | PCSL Implementation |
|-------------|---------------------|
| Test Planning | EP definition with targets, fixtures, sampling config |
| Test Design | ES creation with structural, semantic, and judge checks |
| Test Implementation | PD creation with prompt template and I/O expectations |
| Test Execution | ContractRunner with sampling, repair policies |
| Test Reporting | CLI/JSON/JUnit reporters with metrics and CI |

### 29119-3: Test Documentation

PCSL provides comprehensive test documentation:

- **Test Plan**: EP file (targets, execution mode, sampling strategy)
- **Test Specification**: ES file (checks, constraints, budgets)
- **Test Case**: Combination of PD + ES + EP fixtures
- **Test Log**: Artifacts saved to `save_io_dir` (run.json, inputs, outputs)
- **Test Report**: JSON/JUnit output with pass rates, latency, confidence intervals

### 29119-4: Test Techniques

| ISO Technique | PCSL Feature |
|---------------|--------------|
| Specification-based | json_required, enum, regex checks |
| Structure-based | JSON schema enforcement in enforce mode |
| Experience-based | LLM-as-judge for semantic quality |
| Risk-based | Latency budgets, token budgets |
| Statistical | N-sampling with bootstrap confidence intervals |

## EU AI Act Compliance

### Article 9: Risk Management System

**Requirement**: AI systems must implement risk management processes.

**PCSL Support**:
- **pc.check.latency_budget**: Monitor response time risks
- **pc.check.token_budget**: Control resource consumption risks
- **N-sampling with CI**: Quantify reliability with statistical confidence
- **repair_policy**: Define automated mitigation strategies
- **is_nonenforceable flag**: Explicitly mark when constraints cannot be enforced

### Article 10: Data and Data Governance

**Requirement**: Training, validation, and testing datasets must be subject to data governance.

**PCSL Support**:
- **Fixtures**: Versioned test datasets in EP
- **Gold labels**: Optional ground truth for task accuracy metrics
- **save_io_dir**: Complete audit trail of inputs/outputs
- **prompt_hash**: Cryptographic verification of test inputs

### Article 12: Record-Keeping

**Requirement**: High-risk AI systems must maintain logs enabling traceability.

**PCSL Support**:
- **run.json**: Comprehensive execution metadata
  - Timestamp (ISO 8601)
  - PCSL version
  - Target (model, provider, params)
  - Execution mode (requested vs effective)
  - Check results with pass/fail verdicts
  - Repair ledger (all transformations applied)
  - Capability negotiation logs
- **Artifact paths**: Absolute paths to all I/O files
- **Immutable hashes**: SHA-256 of prompts for tamper detection

### Article 13: Transparency and Provision of Information

**Requirement**: Users must be informed about AI system capabilities and limitations.

**PCSL Support**:
- **Capability negotiation**: Formal μ(Acap, Mreq) → Mactual mapping
- **negotiation_log**: Detailed reasoning for mode fallbacks
- **is_nonenforceable**: Explicit notification when enforce mode unavailable
- **provider_consistency metric**: Measure output variability across samples

### Article 14: Human Oversight

**Requirement**: High-risk AI systems must be designed for human oversight.

**PCSL Support**:
- **assist mode**: Provides guidance without hard constraints
- **observe mode**: Pure monitoring without intervention
- **LLM-as-judge**: Humans can define quality criteria via natural language
- **Repair ledger**: Transparency into automated corrections

### Article 15: Accuracy, Robustness, and Cybersecurity

**Requirement**: AI systems must achieve appropriate levels of accuracy and robustness.

**PCSL Support**:
- **task_accuracy metric**: Compare outputs to gold labels (exact match)
- **validation_success metric**: Percentage passing all checks
- **N-sampling**: Robustness via repeated execution with aggregation
- **Bootstrap CI**: Statistical confidence bounds on reliability
- **Seed reproducibility**: Deterministic execution for security audits

## IEEE 730: Software Quality Assurance

### SQA Plan Elements

| IEEE 730 Element | PCSL Implementation |
|------------------|---------------------|
| Purpose | Defined in PD.description, ES.description |
| Test Approach | EP.execution.mode (observe/assist/enforce) |
| Test Criteria | ES.checks with pass thresholds |
| Test Environment | EP.targets (provider, model, params) |
| Test Data | EP.fixtures with input + optional gold labels |

### Quality Records

All execution artifacts comply with IEEE 730 quality record requirements:
- Version control (pcsl field in all artifacts)
- Traceability (fixture_id linking inputs to outputs)
- Reproducibility (seed + params)
- Configuration management (artifact_paths)

## NIST AI Risk Management Framework

### Measure Function

| NIST Subcategory | PCSL Metric |
|------------------|-------------|
| MEASURE 2.1: Test datasets are used to evaluate performance | fixtures in EP |
| MEASURE 2.2: Evaluations are statistically valid | bootstrap CI from N-sampling |
| MEASURE 2.3: AI systems are evaluated for resilience | repair_rate metric |
| MEASURE 2.8: Risks from AI system outputs are identified | check failures trigger RED status |

### Govern Function

- **GOVERN 3.1**: Appropriate methods for AI deployment are followed
  - Capability negotiation prevents deployment of unenforceable modes
  - strict_enforce flag ensures no silent degradation

- **GOVERN 4.1**: Accountability structures are in place
  - All executions logged with timestamp, target, params
  - artifact_paths enable forensic analysis

## Regulatory Compliance Checklist

### For Regulated Industries (Healthcare, Finance, etc.)

- [x] **Deterministic Testing**: Seed-based reproducibility
- [x] **Audit Trail**: Complete I/O logging with hashes
- [x] **Statistical Validation**: Bootstrap confidence intervals
- [x] **Quality Metrics**: validation_success, task_accuracy, repair_rate
- [x] **Risk Monitoring**: Latency/token budgets with alerts (RED status)
- [x] **Transparency**: Capability negotiation logs, repair ledgers
- [x] **Human Oversight**: observe/assist modes, LLM-as-judge
- [x] **Versioning**: PCSL version tracked in all artifacts

### For AI System Providers

- [x] **Model Capability Documentation**: Formal capability structs
- [x] **Performance Benchmarks**: Comprehensive metrics per target
- [x] **Failure Analysis**: Check results with detailed messages
- [x] **Robustness Testing**: N-sampling with aggregation policies
- [x] **Deployment Modes**: observe (monitoring) → assist (guidance) → enforce (hard constraints)

## Standards Compliance Matrix

| Standard | Scope | PCSL Coverage |
|----------|-------|---------------|
| ISO/IEC/IEEE 29119 | Software Testing | Complete |
| EU AI Act | AI System Compliance | Articles 9, 10, 12, 13, 14, 15 |
| IEEE 730 | Quality Assurance | SQA Plan + Records |
| NIST AI RMF | Risk Management | Measure + Govern functions |
| ISO/IEC 25010 | Product Quality | Reliability, Maintainability, Portability |

## Risk Matrix Example (EU AI Act Article 9)

### Risk Assessment for Medical Diagnosis Assistant

| Risk Category | Likelihood | Severity | PCSL Mitigation | Status |
|---------------|------------|----------|-----------------|--------|
| Hallucination | High | Critical | `json_required`, `enum`, enforce mode | MITIGATED |
| Latency Spike | Medium | High | `pc.check.latency_budget` (2s) | MONITORED |
| Token Overflow | Low | Medium | `pc.check.token_budget` (500) | CONTROLLED |
| Schema Drift | Medium | Critical | N-sampling (N=5), bootstrap CI | VALIDATED |
| Repair Failure | Low | High | `repair_ledger` tracking, alerts | TRANSPARENT |

**Risk Score Calculation**:
```
Risk = Likelihood × Severity × (1 - Mitigation_Effectiveness)
```

**PCSL Configuration**:
```json
{
  "execution": {
    "mode": "enforce",
    "strict_enforce": true,
    "max_retries": 2
  },
  "sampling": {
    "n": 5,
    "aggregation": "majority",
    "confidence_level": 0.95
  }
}
```

### Human Oversight Roles (Article 14)

| Role | Mode | Responsibility | PCSL Support |
|------|------|----------------|--------------|
| Developer | observe | Define contracts, monitor metrics | ES creation, CLI reports |
| QA Engineer | assist | Validate prompts, review failures | Artifact analysis, repair ledger |
| Compliance Officer | enforce | Ensure regulatory adherence | Audit JSON, capability logs |
| Domain Expert | assist/enforce | Review edge cases, set thresholds | LLM-as-judge, gold labels |

---

## Audit Bundle Example

### Complete Audit Package Structure

```
audit_bundle_20250109_143022/
├── audit_manifest.json          # SHA256 hashes + metadata
├── prompt_definition.json       # PD artifact
├── expectation_suite.json       # ES artifact
├── evaluation_profile.json      # EP artifact
├── run.json                     # Execution log
├── fixtures/
│   ├── input_001.txt
│   ├── input_002.txt
│   └── ...
├── outputs/
│   ├── output_001.json
│   ├── output_002.json
│   └── ...
└── checksums.txt                # Line-by-line SHA256 verification
```

### audit_manifest.json

```json
{
  "audit_id": "audit_20250109_143022",
  "pcsl_version": "0.3.1",
  "created_at": "2025-01-09T14:30:22.123Z",
  "purpose": "Regulatory compliance audit for medical diagnosis assistant",
  "system_under_test": {
    "prompt_id": "med_diag.v2.5",
    "provider": "openai",
    "model": "gpt-4o-mini",
    "capabilities": {
      "schema_guided_json": true,
      "supports_seed": true
    }
  },
  "execution": {
    "mode": "enforce",
    "strict_enforce": true,
    "fixtures_count": 200,
    "seed": 42,
    "sampling": {
      "n": 5,
      "aggregation": "majority"
    }
  },
  "results": {
    "validation_success": 0.965,
    "task_accuracy": 0.942,
    "repair_rate": 0.018,
    "avg_latency_ms": 387,
    "confidence_interval": [0.954, 0.976]
  },
  "checksums": {
    "prompt_definition": "sha256:a3f2c8d1e9b4f6a7c2d8e1f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3",
    "expectation_suite": "sha256:b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3",
    "evaluation_profile": "sha256:c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4",
    "run_json": "sha256:d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5",
    "fixtures_archive": "sha256:e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0c9d8e7f6",
    "outputs_archive": "sha256:f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7"
  },
  "compliance_tags": [
    "ISO-29119-compliant",
    "EU-AI-Act-Article-12",
    "NIST-AI-RMF-Measure-2.2"
  ],
  "auditor": {
    "name": "Compliance Verification System",
    "version": "1.0.0",
    "timestamp": "2025-01-09T14:30:22.123Z"
  },
  "signature": "gpg:0x1234567890ABCDEF"
}
```

### Generating Audit Bundle

```bash
# Run evaluation with audit mode
prompt-contracts run \
  --pd prompts/med_diag_pd.json \
  --es prompts/med_diag_es.json \
  --ep prompts/med_diag_ep.json \
  --save-io artifacts/audit_$(date +%Y%m%d_%H%M%S) \
  --seed 42 \
  --n 5 \
  --report json \
  --out audit_report.json

# Generate checksums
cd artifacts/audit_20250109_143022
find . -type f -exec sha256sum {} \; > checksums.txt

# Create audit manifest
python scripts/create_audit_manifest.py \
  --run-json run.json \
  --checksums checksums.txt \
  --output audit_manifest.json

# Sign bundle (optional)
gpg --detach-sign --armor audit_manifest.json
```

### Verification

```bash
# Verify checksums
sha256sum -c checksums.txt

# Verify GPG signature (if signed)
gpg --verify audit_manifest.json.asc audit_manifest.json

# Validate PCSL artifacts
prompt-contracts validate \
  --pd prompt_definition.json \
  --es expectation_suite.json \
  --ep evaluation_profile.json
```

---

## SHA256 Hash Computation

### Prompt Hash (for tamper detection)

```python
import hashlib
import json

def compute_prompt_hash(pd: dict, fixture: dict) -> str:
    """
    Compute SHA256 hash of final prompt for audit trail.

    Args:
        pd: Prompt Definition
        fixture: Input fixture

    Returns:
        Hex string of SHA256 hash
    """
    # Construct final prompt
    prompt_text = pd["prompt"]
    if fixture.get("input"):
        prompt_text = f"{prompt_text}\n\nInput: {fixture['input']}"

    # Canonical JSON for reproducibility
    canonical = json.dumps(
        {"prompt": prompt_text, "fixture_id": fixture["id"]},
        sort_keys=True,
        separators=(',', ':')
    )

    # Compute hash
    return hashlib.sha256(canonical.encode('utf-8')).hexdigest()
```

### Artifact Hash (for integrity verification)

```python
def compute_artifact_hash(artifact_path: str) -> str:
    """Compute SHA256 of artifact file."""
    sha256_hash = hashlib.sha256()
    with open(artifact_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()
```

### Usage in run.json

```json
{
  "fixture_id": "fix_001",
  "prompt_hash": "a3f2c8d1e9b4f6a7c2d8e1f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3",
  "output_hash": "b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3",
  "timestamp": "2025-01-09T14:30:22.123Z",
  "checks": [...],
  "status": "GREEN"
}
```

---

## Compliance Statement Template

For organizations using prompt-contracts in regulated environments:

```
COMPLIANCE STATEMENT

Organization: [Your Organization Name]
System: [AI System Name and Version]
Date: [YYYY-MM-DD]

This system has been evaluated using prompt-contracts v0.3.1, which implements:

1. ISO/IEC/IEEE 29119 Software Testing Standards
   - Test planning, design, implementation, execution, and reporting
   - Statistical test techniques (bootstrap CI)

2. EU AI Act Compliance (Regulation 2024/XXX)
   - Article 9: Risk management with latency/token budgets
   - Article 10: Data governance via versioned fixtures
   - Article 12: Complete audit trails with SHA256 hashes
   - Article 13: Transparency via capability negotiation
   - Article 14: Human oversight modes (observe/assist/enforce)
   - Article 15: Statistical accuracy validation (bootstrap CI)

3. IEEE 730 Software Quality Assurance
   - Quality records with version control and traceability
   - Reproducibility via seed-based execution

4. NIST AI Risk Management Framework
   - MEASURE 2.2: Statistically valid evaluations
   - GOVERN 3.1: Appropriate deployment methods

Audit Bundle: [SHA256 hash of audit_manifest.json]
Results: [validation_success]% validation success, [task_accuracy]% task accuracy
Confidence Interval: [CI_lower, CI_upper] (95% bootstrap)

Certification: This evaluation was conducted in accordance with the above standards
and regulatory requirements. All artifacts are available for independent verification.

Signed: ___________________________
        [Name, Title]
        [Organization]
        [Date]
```

---

## Limitations

- **PCSL does not provide**: Fairness/bias testing, adversarial robustness, data privacy controls
- **Recommendation**: Combine PCSL with domain-specific tools (e.g., fairness metrics, differential privacy)

## References

1. ISO/IEC/IEEE 29119-1:2022 - Software Testing - Part 1: Concepts and definitions
2. EU AI Act (2024) - Regulation on Artificial Intelligence
3. IEEE 730-2014 - Software Quality Assurance Processes
4. NIST AI Risk Management Framework (AI RMF 1.0)
5. ISO/IEC 25010:2011 - Systems and software Quality Requirements and Evaluation (SQuaRE)

---

**Document Version**: 1.1.0
**PCSL Version**: 0.3.1
**Last Updated**: 2025-01-09
