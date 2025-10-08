# PyPI Setup Guide (Schritt für Schritt)

## Was du brauchst

Der Workflow ist **bereits fertig** und wartet nur auf dein PyPI Setup!

## Schritt 1: PyPI Trusted Publisher

### 1.1 Gehe zu PyPI
👉 https://pypi.org/manage/account/publishing/

### 1.2 Klick "Add a new pending publisher"

### 1.3 Fülle das Formular aus

**EXAKT diese Werte:**

```
PyPI Project Name:    prompt-contracts
Owner:               philippmelikidis        ← WICHTIG: klein p!
Repository name:     prompt-contracts
Workflow name:       publish-pypi.yml        ← EXAKT so!
Environment name:    pypi
```

**Screenshot-Hilfe:**
- PyPI Project Name = Name auf PyPI (wird erstellt beim ersten Upload)
- Owner = Dein GitHub Username (klein p!)
- Repository name = Dein Repo-Name
- Workflow name = Dateiname in `.github/workflows/`
- Environment name = GitHub Environment (Schritt 2)

### 1.4 Klick "Add"

✅ Fertig! PyPI weiß jetzt dass dein GitHub Repo uploaden darf.

---

## Schritt 2: GitHub Environment

### 2.1 Gehe zu GitHub Settings
👉 https://github.com/philippmelikidis/prompt-contracts/settings/environments

### 2.2 Klick "New environment"

### 2.3 Name eingeben
```
Name: pypi
```

### 2.4 Klick "Configure environment"

**Optional (aber empfohlen):**
- Protection rules: Required reviewers (wenn du möchtest)
- Deployment branches: Only protected branches

✅ Fertig! GitHub weiß jetzt dass der Workflow dieses Environment nutzen darf.

---

## Schritt 3: GitHub Release

### 3.1 Gehe zu Releases
👉 https://github.com/philippmelikidis/prompt-contracts/releases/new

### 3.2 Fülle das Release-Formular aus

**Tag:**
```
v0.2.0
```

**Target:**
```
dev
```
(oder `main` wenn du den Code gemerged hast)

**Title:**
```
Release v0.2.0
```

**Description:**
```markdown
## What's New

### Features
- Professional v0.2.0 release
- Full PCSL (Prompt Contract Specification Language) implementation
- Execution modes: observe, assist, enforce, auto
- Auto-repair & bounded retries
- Multi-target testing (OpenAI, Ollama)
- Comprehensive CI/CD pipeline

### Installation
```bash
pip install prompt-contracts
```

### Quick Start
See [QUICKSTART.md](./QUICKSTART.md) for detailed examples.

### Documentation
- [README.md](./README.md) - Overview
- [CONTRIBUTING.md](./CONTRIBUTING.md) - Development guide
- [CHANGELOG.md](./CHANGELOG.md) - Version history
```

### 3.3 Optionen

✅ **WICHTIG:** "Set as the latest release" anhaken!

### 3.4 Klick "Publish release"

🚀 **FERTIG!** Der Workflow startet jetzt automatisch!

---

## Schritt 4: Verify

### 4.1 Check GitHub Actions
👉 https://github.com/philippmelikidis/prompt-contracts/actions

Du solltest sehen:
- ✅ Workflow "Publish to PyPI" läuft
- Nach ~2 Minuten: ✅ Grünes Häkchen

### 4.2 Check PyPI
👉 https://pypi.org/project/prompt-contracts/

Dein Package sollte jetzt live sein! 🎉

### 4.3 Test Installation

```bash
# In neuem Terminal / neuer Umgebung
pip install prompt-contracts
prompt-contracts --version
# Sollte ausgeben: 0.2.0
```

---

## Troubleshooting

### ❌ "Publishing is not configured for this user/organization"
→ Schritt 1 noch nicht gemacht (PyPI Trusted Publisher)

### ❌ "Environment protection rules not satisfied"
→ Schritt 2 noch nicht gemacht (GitHub Environment)

### ❌ "Workflow does not have permission to publish"
→ Check `.github/workflows/publish-pypi.yml`:
  - `permissions: id-token: write` muss da sein ✅
  - `environment: name: pypi` muss da sein ✅

### ❌ "Version 0.2.0 already exists on PyPI"
→ Bumpe die Version in `pyproject.toml` zu `0.2.1`
→ Erstelle neuen Release `v0.2.1`

---

## Warum Trusted Publisher?

**Vorteile:**
- ✅ Keine API Tokens speichern
- ✅ Automatisch bei jedem Release
- ✅ Sicherer (OpenID Connect)
- ✅ Transparent (alles in GitHub Actions sichtbar)
- ✅ PyPI's empfohlene Methode seit 2023

**Alte Methode (NICHT empfohlen):**
- ❌ API Token generieren
- ❌ In GitHub Secrets speichern
- ❌ Manuell rotieren
- ❌ Security Risk

---

## Nächste Releases

Für alle zukünftigen Releases:

1. Bumpe Version in `pyproject.toml`: `0.2.0` → `0.2.1`
2. Commit & Push
3. GitHub Release erstellen (Tag `v0.2.1`)
4. → **Automatischer PyPI Upload!** 🎉

Kein Setup mehr nötig!

