#!/bin/bash
set -e

echo "🧪 Schritt 1: Tests ausführen..."
source .venv/bin/activate
pytest -v

echo ""
echo "🎨 Schritt 2: Code-Formatierung prüfen..."
black --check promptcontracts/ tests/ || (echo "❌ Black-Formatierung nötig. Führe aus: make format" && exit 1)
isort --check-only promptcontracts/ tests/ || (echo "❌ isort nötig. Führe aus: make format" && exit 1)
ruff check promptcontracts/ tests/ || (echo "❌ Ruff-Fehler gefunden" && exit 1)

echo ""
echo "✅ Schritt 3: Beispiele validieren..."
prompt-contracts validate pd examples/support_ticket/pd.json
prompt-contracts validate es examples/support_ticket/es.json
prompt-contracts validate ep examples/support_ticket/ep.json

echo ""
echo "📦 Schritt 4: Package bauen..."
python -m build

echo ""
echo "🔍 Schritt 5: Package prüfen..."
twine check dist/*

echo ""
echo "✅ Alle Checks erfolgreich! Bereit für Release."
