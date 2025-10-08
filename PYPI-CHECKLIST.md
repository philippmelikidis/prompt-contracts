# 🚀 PyPI Publishing Checklist

## Vorbereitung (einmalig)

- [ ] **PyPI Account erstellen**
  - → https://pypi.org/account/register/
  - Email bestätigen

- [ ] **Trusted Publisher einrichten**
  - → https://pypi.org/manage/account/publishing/
  - "Add a new pending publisher"
  - Eingaben:
    ```
    PyPI Project Name:    prompt-contracts
    Owner:               philippmelikidis
    Repository name:     prompt-contracts
    Workflow name:       publish-pypi.yml
    Environment name:    pypi
    ```

- [ ] **GitHub Environment anlegen**
  - → https://github.com/philippmelikidis/prompt-contracts/settings/environments
  - New environment: `pypi`
  - (Optional) Protection rules konfigurieren

## Release erstellen

- [ ] **Version bump** (falls nötig)
  ```bash
  # In pyproject.toml: version = "0.2.0" → "0.2.1"
  git add pyproject.toml
  git commit -m "Bump version to 0.2.1"
  git push origin dev
  ```

- [ ] **GitHub Release erstellen**
  - → https://github.com/philippmelikidis/prompt-contracts/releases/new
  - Tag: `v0.2.0` (oder aktuelle Version)
  - Target: `dev` (oder `main`)
  - Title: `Release v0.2.0`
  - Description: Release notes einfügen (siehe GITHUB-RELEASE-GUIDE.md)
  - ✅ "Set as the latest release"
  - **Publish release** klicken

## Verify

- [ ] **GitHub Action prüfen**
  - → https://github.com/philippmelikidis/prompt-contracts/actions
  - Workflow "Publish to PyPI" sollte grün sein ✅

- [ ] **PyPI Package prüfen**
  - → https://pypi.org/project/prompt-contracts/
  - Version sollte sichtbar sein

- [ ] **Installation testen**
  ```bash
  pip install prompt-contracts
  prompt-contracts --version
  ```

## Troubleshooting

### ❌ "Publishing is not configured for this user/organization"
→ Trusted Publisher auf PyPI noch nicht eingerichtet (Schritt 2)

### ❌ "Environment protection rules not satisfied"
→ GitHub Environment `pypi` fehlt (Schritt 3)

### ❌ "Workflow does not have permission to publish"
→ Check `permissions: id-token: write` in `.github/workflows/publish-pypi.yml`

### ❌ "Version already exists"
→ Version in `pyproject.toml` bumpen und neuen Release erstellen

## Nächste Releases

Für alle zukünftigen Releases:

1. Version bumpen in `pyproject.toml`
2. Commit + Push
3. GitHub Release erstellen
4. → **Automatischer PyPI Upload!** 🎉

---

📚 **Weitere Hilfe:**
- [GITHUB-RELEASE-GUIDE.md](./GITHUB-RELEASE-GUIDE.md) - Detaillierte Release-Anleitung
- [PyPI Docs](https://docs.pypi.org/trusted-publishers/) - Trusted Publishers Dokumentation
