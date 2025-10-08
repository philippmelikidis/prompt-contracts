# GitHub Release erstellen - Schritt für Schritt

## 📍 Schritt 1: Zum Release-Bereich navigieren

1. Öffne deinen Browser
2. Gehe zu: **https://github.com/philippmelikidis/prompt-contracts**
3. Klicke rechts auf **"Releases"** (in der Sidebar)
4. Klicke auf **"Create a new release"** oder **"Draft a new release"**

## 📝 Schritt 2: Release-Formular ausfüllen

### A) Tag auswählen
- **Dropdown "Choose a tag"**: Wähle `v0.2.0` aus
- Falls nicht sichtbar: Gib `v0.2.0` ein und wähle den existierenden Tag

### B) Release-Titel
```
v0.2.0 - Professional Package Structure
```

### C) Beschreibung (kopiere das hier rein):

```markdown
## What's New in v0.2.0

This release transforms prompt-contracts into a professional, production-ready Python package with enhanced execution modes, auto-repair capabilities, and comprehensive developer tooling.

### 🎯 Major Features

#### Public Python API
```python
from promptcontracts import run_contract, validate_artifact

# Run a contract programmatically
results = run_contract(
    pd="examples/support_ticket/pd.json",
    es="examples/support_ticket/es.json",
    ep="examples/support_ticket/ep.json"
)

# Validate artifacts
validate_artifact('pd', 'path/to/pd.json')
```

#### Execution Modes
- **observe**: Validation-only mode (no enforcement)
- **assist**: Prompt augmentation with constraint injection
- **enforce**: Schema-guided JSON generation (OpenAI)
- **auto**: Automatic fallback based on adapter capabilities

#### Auto-Repair & Normalization
- Automatic markdown fence stripping (` ```json ... ``` `)
- JSONPath field lowercasing (e.g., `"High" → "high"`)
- Bounded retries with exponential backoff
- Status codes: `PASS`, `REPAIRED`, `FAIL`, `NONENFORCEABLE`

### ✨ New Components

- **Custom Error Classes**: `SpecValidationError`, `AdapterError`, `ExecutionError`, `CheckFailure`
- **Utility Modules**: Normalization, retry logic, hashing, timestamps
- **GitHub Templates**: Bug reports, feature requests, PR template, release checklist
- **CI/CD Pipeline**: GitHub Actions workflow (lint + test + build)
- **Pre-commit Hooks**: Black, isort, Ruff integration

### 🔧 Developer Experience

- `Makefile` with helpful commands (`make help`)
- Professional `CONTRIBUTING.md` guide
- `CODEOWNERS` configuration
- `.editorconfig` for consistent coding style
- Comprehensive documentation in `RELEASE.md`

### 📦 Package Improvements

- Fixed license configuration (SPDX-compliant)
- Updated to v0.2.0 across all files
- All linting issues resolved
- Code formatted with Black + isort

### 📊 Test Coverage

- **47 tests** passing
- **35.84%** overall coverage
- Core utilities: **97.44%** coverage (normalization)
- Validator: **72.58%** coverage

### 🆕 What's Coming Next (v0.3.0)

- Integration tests with real LLM calls
- HTML reporter with visual diffs
- Enhanced schema derivation (nested properties)
- Security checks (L4 conformance)
- PyPI publication

### 📚 Documentation

- Updated `README.md` with badges and professional structure
- New `CHANGELOG.md` tracking all changes
- `QUICKSTART.md` for new users
- Complete API documentation in docstrings

### ⚠️ Breaking Changes

**None** - This release is fully backwards compatible with v0.1.0

### 🔗 Links

- **Documentation**: [README.md](https://github.com/philippmelikidis/prompt-contracts/blob/dev/README.md)
- **Quickstart**: [QUICKSTART.md](https://github.com/philippmelikidis/prompt-contracts/blob/dev/QUICKSTART.md)
- **Contributing**: [CONTRIBUTING.md](https://github.com/philippmelikidis/prompt-contracts/blob/dev/CONTRIBUTING.md)
- **Spec**: [PCSL v0.1](https://github.com/philippmelikidis/prompt-contracts/blob/dev/src/promptcontracts/spec/pcsl-v0.1.md)

### 🙏 Thank You

Thanks to everyone who contributed ideas and feedback for this release!

---

**Full Changelog**: [v0.1.0...v0.2.0](https://github.com/philippmelikidis/prompt-contracts/compare/v0.1.0...v0.2.0)
```

### D) Dateien hochladen (Optional)

Du kannst die Build-Artefakte anhängen:

1. Klicke auf **"Attach binaries by dropping them here or selecting them"**
2. Wähle diese Dateien aus deinem `dist/` Ordner:
   - `prompt_contracts-0.2.0.tar.gz`
   - `prompt_contracts-0.2.0-py3-none-any.whl`

**Wichtig**: Die Dateien müssen erst gebaut werden! Führe aus:
```bash
cd /Users/PhilipposMelikidis/Desktop/prompt-contracts
source .venv/bin/activate
rm -rf dist/ build/
python -m build
```

### E) Release-Optionen

- ✅ **"Set as the latest release"** - Ankreuzen!
- ❌ **"Set as a pre-release"** - NICHT ankreuzen
- ❌ **"Create a discussion for this release"** - Optional

## 🚀 Schritt 3: Veröffentlichen

1. Klicke auf **"Publish release"**
2. Fertig! 🎉

## 🔍 Nach dem Release

### Was passiert jetzt?

1. **Release ist öffentlich sichtbar**:
   - https://github.com/philippmelikidis/prompt-contracts/releases

2. **Tag ist verfügbar**:
   ```bash
   git clone https://github.com/philippmelikidis/prompt-contracts.git
   git checkout v0.2.0
   ```

3. **Nutzer können installieren**:
   ```bash
   # Direkt von GitHub
   pip install git+https://github.com/philippmelikidis/prompt-contracts.git@v0.2.0

   # Oder von den Release-Artefakten
   pip install prompt_contracts-0.2.0-py3-none-any.whl
   ```

### Optional: PyPI Upload

Falls du das Package öffentlich auf PyPI veröffentlichen willst:

```bash
# 1. PyPI Account erstellen: https://pypi.org/account/register/
# 2. API Token erstellen: https://pypi.org/manage/account/token/
# 3. Upload
twine upload dist/*
```

Dann kann jeder installieren mit:
```bash
pip install prompt-contracts
```

## ❓ Häufige Probleme

### Problem: "Tag already exists"
- **Lösung**: Wähle den existierenden Tag `v0.2.0` aus dem Dropdown

### Problem: "Can't upload files"
- **Lösung**: Baue erst das Package mit `python -m build`

### Problem: "Release not visible"
- **Lösung**: Stelle sicher, dass "Set as latest release" aktiviert ist

## 📸 Screenshots-Guide (falls unklar)

Falls du visuelle Hilfe brauchst:

1. **Release-Button finden**: Auf der Hauptseite rechts in der Sidebar
2. **Create release**: Grüner Button oben rechts
3. **Tag wählen**: Dropdown-Menü mit allen Tags
4. **Publish**: Großer grüner Button am Ende des Formulars

---

**Viel Erfolg! 🎉**
