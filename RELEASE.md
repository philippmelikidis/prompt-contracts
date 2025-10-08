# Release Guide - prompt-contracts v0.2.0

Komplette Anleitung für das Veröffentlichen von v0.2.0.

## 📋 Pre-Release Checklist

### 1. Alle Tests ausführen
```bash
make test-cov
```
✅ Erwartetes Ergebnis: 47 tests passed

### 2. Code-Qualität prüfen
```bash
make lint
# oder
make format  # Auto-fix
```

### 3. Beispiele validieren
```bash
make validate-examples
```

### 4. Package bauen
```bash
make build
```
Erstellt:
- `dist/prompt_contracts-0.2.0.tar.gz` (Source Distribution)
- `dist/prompt_contracts-0.2.0-py3-none-any.whl` (Wheel)

### 5. Package testen
```bash
# In einer neuen Virtual Environment
python -m venv test-env
source test-env/bin/activate
pip install dist/prompt_contracts-0.2.0-py3-none-any.whl

# Testen
prompt-contracts --version
prompt-contracts validate pd examples/support_ticket/pd.json

# Cleanup
deactivate
rm -rf test-env
```

## 🚀 Release auf GitHub

### Schritt 1: Änderungen committen
```bash
# Alle Änderungen stagen
git add .

# Status prüfen
git status

# Commit mit konventioneller Message
git commit -m "feat: v0.2.0 - professional package structure with public API

- Add public API (run_contract, validate_artifact)
- Implement execution modes (auto, enforce, assist, observe)
- Add auto-repair utilities (normalization, retry)
- Add custom error classes (SpecValidationError, etc.)
- Add comprehensive GitHub templates (issues, PRs)
- Add CI/CD pipeline with GitHub Actions
- Add pre-commit hooks configuration
- Add professional documentation (CONTRIBUTING.md, CHANGELOG.md)
- Extend tests for new features (47 tests passing)
- Update version to 0.2.0

Breaking changes: None (backwards compatible with 0.1.0)"
```

### Schritt 2: Tag erstellen
```bash
# Alten Tag löschen (falls vorhanden)
git tag -d v0.2.0 2>/dev/null || true

# Neuen Tag erstellen
git tag -a v0.2.0 -m "Release v0.2.0: Professional package structure"

# Tags anzeigen
git tag
```

### Schritt 3: Zu GitHub pushen
```bash
# Aktuellen Branch pushen
git push origin dev

# Tag pushen
git push origin v0.2.0

# Oder beides zusammen
git push origin dev --tags
```

### Schritt 4: GitHub Release erstellen

1. Gehe zu: https://github.com/PhilipposMelikidis/prompt-contracts/releases
2. Klicke auf "Draft a new release"
3. Tag wählen: `v0.2.0`
4. Release Title: `v0.2.0 - Professional Package Structure`
5. Description aus CHANGELOG.md kopieren
6. Artefakte anhängen:
   - `dist/prompt_contracts-0.2.0.tar.gz`
   - `dist/prompt_contracts-0.2.0-py3-none-any.whl`
7. "Publish release" klicken

## 📦 Optional: PyPI Upload

⚠️ **Achtung**: Nur ausführen, wenn du das Package auf PyPI veröffentlichen willst!

### TestPyPI (zum Testen)
```bash
# 1. Account erstellen auf https://test.pypi.org/account/register/
# 2. API Token erstellen
# 3. Upload
twine upload --repository testpypi dist/*

# 4. Installieren und testen
pip install --index-url https://test.pypi.org/simple/ prompt-contracts
```

### Produktions-PyPI
```bash
# 1. Account erstellen auf https://pypi.org/account/register/
# 2. API Token erstellen und in ~/.pypirc speichern
# 3. Upload
twine upload dist/*

# 4. Weltweit verfügbar
pip install prompt-contracts
```

## 🔍 Post-Release Validierung

### 1. CI/CD prüfen
- GitHub Actions: https://github.com/PhilipposMelikidis/prompt-contracts/actions
- Alle Workflows sollten ✅ grün sein

### 2. Installation testen
```bash
# Frische Installation
pip install prompt-contracts==0.2.0
prompt-contracts --version
# Sollte ausgeben: prompt-contracts 0.2.0
```

### 3. Dokumentation aktualisieren
- [ ] README.md Badges aktualisieren
- [ ] CHANGELOG.md "Unreleased" → "0.2.0" umbenennen
- [ ] Nächste Version planen (0.3.0 oder 1.0.0?)

## 📊 Quick Commands

```bash
# Alles in einem: Test → Build → Check
make release-check

# Lokales Package installieren
pip install -e ".[dev]"

# Package neu bauen (nach Änderungen)
rm -rf dist/ build/
make build

# Pre-commit Hooks updaten
pre-commit autoupdate
pre-commit run --all-files
```

## 🐛 Troubleshooting

### Problem: "Tag already exists"
```bash
# Lokalen Tag löschen
git tag -d v0.2.0

# Remote Tag löschen (Vorsicht!)
git push origin :refs/tags/v0.2.0

# Neu erstellen
git tag -a v0.2.0 -m "Release v0.2.0"
git push origin v0.2.0
```

### Problem: "Module not found" nach Installation
```bash
# Editable Install erneuern
pip uninstall prompt-contracts
pip install -e .

# Oder normaler Install
pip install dist/prompt_contracts-0.2.0-py3-none-any.whl
```

### Problem: Pre-commit Hooks schlagen fehl
```bash
# Hooks neu installieren
pre-commit uninstall
pre-commit install

# Manuell formatieren
make format

# Dann nochmal committen
git add .
git commit --amend --no-edit
```

## ✅ Success Criteria

- [x] Alle 47 Tests bestehen
- [x] Package erfolgreich gebaut
- [x] `twine check` ohne Fehler
- [x] Git Tag erstellt
- [x] Zu GitHub gepusht
- [ ] GitHub Release erstellt
- [ ] CI/CD grün
- [ ] (Optional) PyPI Upload erfolgreich

---

**Version**: 0.2.0
**Datum**: 2025-10-08
**Maintainer**: Philippos Melikidis
