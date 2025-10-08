#!/bin/bash
# Setup Git Remote für GitHub

echo "🔧 Git Remote Setup"
echo ""
echo "Dieses Script hilft dir, dein GitHub Remote zu konfigurieren."
echo ""

# Check if remote already exists
if git remote get-url origin &> /dev/null; then
    echo "ℹ️  Remote 'origin' ist bereits konfiguriert:"
    git remote -v
    echo ""
    read -p "Möchtest du es neu setzen? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git remote remove origin
    else
        echo "Abgebrochen."
        exit 0
    fi
fi

echo ""
echo "📝 Bitte gib deine GitHub Repository URL ein."
echo "   Format: https://github.com/USERNAME/REPOSITORY.git"
echo "   oder:   git@github.com:USERNAME/REPOSITORY.git"
echo ""
read -p "GitHub Repository URL: " repo_url

if [ -z "$repo_url" ]; then
    echo "❌ Keine URL eingegeben. Abgebrochen."
    exit 1
fi

# Add remote
git remote add origin "$repo_url"

echo ""
echo "✅ Remote 'origin' hinzugefügt:"
git remote -v
echo ""
echo "🚀 Nächste Schritte:"
echo "  1. Ersten Push (mit upstream setzen):"
echo "     git push -u origin dev"
echo ""
echo "  2. Tag pushen:"
echo "     git push origin v0.2.0"
echo ""
echo "  3. Oder beides zusammen:"
echo "     git push origin dev --tags"
echo ""
