---
name: Release Checklist
about: Checklist for preparing a new release
title: 'Release v[VERSION]'
labels: release
assignees: ''
---

## Release Version
**Target Version**: vX.Y.Z

## Pre-Release Checklist

### Code & Tests
- [ ] All tests passing (`pytest`)
- [ ] Linting passes (`ruff check`, `black --check`, `isort --check`)
- [ ] Pre-commit hooks pass
- [ ] No open critical/blocking issues
- [ ] Performance regression tests completed (if applicable)

### Documentation
- [ ] CHANGELOG.md updated with all changes since last release
- [ ] README.md reflects new features/changes
- [ ] PCSL spec updated (if specification changed)
- [ ] API documentation updated
- [ ] Migration guide written (if breaking changes)

### Version Bumping
- [ ] Version bumped in `pyproject.toml`
- [ ] Version bumped in `src/promptcontracts/__init__.py`
- [ ] CHANGELOG.md has version header and date

### Packaging
- [ ] Build passes: `python -m build`
- [ ] Package installable: `pip install dist/prompt_contracts-X.Y.Z-py3-none-any.whl`
- [ ] CLI works after install: `prompt-contracts --version`
- [ ] Examples run successfully

### Final Steps
- [ ] Create release branch: `release/vX.Y.Z`
- [ ] PR to main with all changes
- [ ] Tag release: `git tag vX.Y.Z`
- [ ] Push tag: `git push origin vX.Y.Z`
- [ ] GitHub release created with changelog
- [ ] PyPI upload: `twine upload dist/*` (if publishing)
- [ ] Announcement (if applicable)

## Notes
Add any special release notes or considerations here.

