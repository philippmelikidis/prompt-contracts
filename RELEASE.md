# Release Guide

## Quick Release Checklist

- [ ] Tests laufen lokal: `make test`
- [ ] Linting passt: `make lint`
- [ ] Package baut: `make build`
- [ ] Version in `pyproject.toml` ist korrekt

## PyPI Setup (einmalig)

### 1. PyPI Account
- Erstelle Account: https://pypi.org/account/register/

### 2. Trusted Publisher (empfohlen, keine Tokens nötig!)
- Gehe zu: https://pypi.org/manage/account/publishing/
- "Add a new pending publisher"
- Eingaben:
  ```
  PyPI Project Name:    prompt-contracts
  Owner:               philippmelikidis
  Repository name:     prompt-contracts
  Workflow name:       publish-pypi.yml
  Environment name:    pypi
  ```

### 3. GitHub Environment
- Gehe zu: https://github.com/philippmelikidis/prompt-contracts/settings/environments
- "New environment"
- Name: `pypi`

## Release erstellen

### GitHub Release (triggert automatisch PyPI Upload)

1. Gehe zu: https://github.com/philippmelikidis/prompt-contracts/releases/new

2. Fülle aus:
   - **Tag**: `v0.3.0` (muss mit pyproject.toml Version übereinstimmen!)
   - **Target**: `dev` oder `main`
   - **Title**: `Release v0.3.0: Probabilistic Contracts & Semantic Validation`
   - **Description**:
     ```markdown
     ## What's New in v0.3.0

     **Major Release** - Probabilistic Contracts & Semantic Validation:

     - **N-Sampling**: Generate multiple samples with configurable aggregation
     - **Bootstrap Confidence Intervals**: Statistical validation with δ=0.95
     - **Semantic Checks**: `contains_all`, `similarity`, `judge` (LLM-as-judge)
     - **Enhanced Parsing**: `json_loose()` and `regex_extract()`
     - **Repair Policies**: Structured normalization with repair ledgers
     - **Compliance Documentation**: ISO/IEC/IEEE 29119, EU AI Act mapping
     - **Formal Capability Negotiation**: μ(Acap, Mreq) → Mactual

     ## Installation
     pip install prompt-contracts

     ## Quick Start
     See QUICKSTART.md for detailed examples.
     ```

3. ✅ "Set as the latest release"

4. Klick **"Publish release"**

5. Check Actions: https://github.com/philippmelikidis/prompt-contracts/actions
   - Workflow "Publish to PyPI" sollte grün werden

6. Nach ~2 Min check PyPI: https://pypi.org/project/prompt-contracts/

## Testen

```bash
# In neuem Terminal/Projekt
pip install prompt-contracts
prompt-contracts --version
```

## Troubleshooting

**❌ "Publishing is not configured"**
→ Trusted Publisher auf PyPI noch nicht eingerichtet (Schritt 2)

**❌ "Environment protection rules not satisfied"**
→ GitHub Environment fehlt (Schritt 3)

**❌ "Version already exists"**
→ Version in `pyproject.toml` bumpen

## Nächster Release

1. Bump Version in `pyproject.toml`: `0.2.0` → `0.2.1`
2. Commit & Push
3. GitHub Release erstellen
4. Fertig! (PyPI Upload ist automatisch)
