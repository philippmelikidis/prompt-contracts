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

**Document Version**: 1.0.0
**PCSL Version**: 0.3.0
**Last Updated**: 2025-01-09
