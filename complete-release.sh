#!/bin/bash
# Kompletter Release-Workflow für v0.2.0

set -e  # Exit on error

echo "🚀 Starting v0.2.0 Release Process"
echo ""

# Aktiviere venv
source .venv/bin/activate

# 1. Tests
echo "1️⃣  Running all tests..."
pytest -q
echo "✅ Tests passed"
echo ""

# 2. Linting
echo "2️⃣  Running code quality checks..."
ruff check promptcontracts/ tests/
echo "✅ Linting passed"
echo ""

# 3. Build
echo "3️⃣  Building package..."
rm -rf dist/ build/
python -m build
echo "✅ Package built"
echo ""

# 4. Check package
echo "4️⃣  Checking package..."
twine check dist/*
echo "✅ Package check passed"
echo ""

# 5. Git commit
echo "5️⃣  Committing changes..."
git add .
git commit -m "feat: v0.2.0 - professional package structure

- Add public API (run_contract, validate_artifact)
- Add execution modes with capability negotiation
- Add auto-repair utilities and custom errors
- Add GitHub templates and CI/CD pipeline
- Add comprehensive documentation
- Fix license configuration and linting issues
- 47 tests passing, 35.56% coverage
- Backwards compatible with v0.1.0"
echo "✅ Changes committed"
echo ""

# 6. Tag
echo "6️⃣  Creating tag..."
git tag -d v0.2.0 2>/dev/null || true  # Delete old tag if exists
git tag -a v0.2.0 -m "Release v0.2.0: Professional package structure"
echo "✅ Tag created: v0.2.0"
echo ""

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║  ✅ Release v0.2.0 is ready!                              ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "📦 Built packages:"
ls -lh dist/
echo ""
echo "🔍 Next steps:"
echo "  1. Push to GitHub:"
echo "     git push origin dev --tags"
echo ""
echo "  2. Create GitHub Release:"
echo "     https://github.com/PhilipposMelikidis/prompt-contracts/releases/new"
echo "     - Tag: v0.2.0"
echo "     - Upload: dist/prompt_contracts-0.2.0.*"
echo ""
echo "  3. (Optional) Publish to PyPI:"
echo "     twine upload dist/*"
echo ""
echo "🎉 Done!"
