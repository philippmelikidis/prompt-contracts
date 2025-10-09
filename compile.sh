#!/bin/bash
# Kompiliere das Paper mit allen Referenzen

cd /Users/PhilipposMelikidis/Desktop/prompt-contracts

echo "=== 1. pdflatex (erstellt .aux) ==="
pdflatex -interaction=nonstopmode prompt_contracts_paper.tex

echo ""
echo "=== 2. bibtex (erstellt .bbl) ==="
bibtex prompt_contracts_paper

echo ""
echo "=== 3. pdflatex (fügt Citations ein) ==="
pdflatex -interaction=nonstopmode prompt_contracts_paper.tex

echo ""
echo "=== 4. pdflatex (final) ==="
pdflatex -interaction=nonstopmode prompt_contracts_paper.tex

echo ""
echo "=== FERTIG! ==="
echo "Prüfe ob references.bib alle Einträge hat:"
grep -c "^@" references.bib 2>/dev/null && echo "Anzahl BibTeX-Einträge in references.bib gefunden" || echo "references.bib nicht gefunden"
