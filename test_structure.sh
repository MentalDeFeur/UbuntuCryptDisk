#!/bin/bash
# Teste la structure du projet transformé
# Usage: bash test_structure.sh

set -e

echo "=== Test de la structure du projet ==="
echo ""

# Test 1 : Vérifier la présence des fichiers essentiels
echo "✓ Test 1 : Fichiers essentiels"
files=(
    "auto_unlock_cryptnux.py"
    "auto_unlock_cryptnux_gui.py"
    "README.md"
    "UBUNTU_README.md"
    "FEDORA_README.md"
    "FLATPAK_README.md"
    "MIGRATION_GUIDE.md"
    "PROJECT_STRUCTURE.md"
    "auto-unlock-cryptnux.spec"
    "build_deb.sh"
    "build_rpm.sh"
    "build_flatpak.sh"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file"
    else
        echo "  ✗ $file (MANQUANT)"
        exit 1
    fi
done

echo ""
echo "✓ Test 2 : Répertoires Flatpak"
flatpak_files=(
    "flatpak/io.github.mentaldefeur.AutoUnlockCryptnux.json"
    "flatpak/io.github.mentaldefeur.AutoUnlockCryptnux.yaml"
    "flatpak/io.github.mentaldefeur.AutoUnlockCryptnux.desktop"
    "flatpak/io.github.mentaldefeur.AutoUnlockCryptnux.metainfo.xml"
    "flatpak/wrapper-cli.sh"
    "flatpak/wrapper-gui.sh"
)

for file in "${flatpak_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file"
    else
        echo "  ✗ $file (MANQUANT)"
        exit 1
    fi
done

echo ""
echo "✓ Test 3 : Permissions des scripts"
scripts=(
    "build_deb.sh"
    "build_rpm.sh"
    "build_flatpak.sh"
    "flatpak/wrapper-cli.sh"
    "flatpak/wrapper-gui.sh"
)

for script in "${scripts[@]}"; do
    if [ -x "$script" ]; then
        echo "  ✓ $script (exécutable)"
    else
        echo "  ! $script (non exécutable, correction en cours...)"
        chmod +x "$script"
        echo "  ✓ $script (rendu exécutable)"
    fi
done

echo ""
echo "✓ Test 4 : Syntaxe JSON Flatpak"
if command -v jq &> /dev/null; then
    if jq empty flatpak/io.github.mentaldefeur.AutoUnlockCryptnux.json 2>/dev/null; then
        echo "  ✓ io.github.mentaldefeur.AutoUnlockCryptnux.json (JSON valide)"
    else
        echo "  ✗ io.github.mentaldefeur.AutoUnlockCryptnux.json (JSON invalide)"
        exit 1
    fi
else
    echo "  ⚠ jq non installé (skip validation JSON)"
fi

echo ""
echo "✓ Test 5 : Vérification .gitignore"
if grep -q "_flatpak_" .gitignore && grep -q "\.flatpak" .gitignore; then
    echo "  ✓ .gitignore contient les entrées Flatpak"
else
    echo "  ✗ .gitignore incomplet"
    exit 1
fi

echo ""
echo "════════════════════════════════════════════"
echo "✓ TOUS LES TESTS RÉUSSIS !"
echo "════════════════════════════════════════════"
echo ""
echo "📊 Résumé de la structure :"
echo "  • Format Ubuntu (Debian)     : build_deb.sh"
echo "  • Format Fedora (RPM)        : build_rpm.sh + auto-unlock-cryptnux.spec"
echo "  • Format Flatpak (multi)     : build_flatpak.sh + flatpak/"
echo ""
echo "🚀 Prochaines étapes :"
echo "  1. Ubuntu   : bash build_deb.sh"
echo "  2. Fedora   : bash build_rpm.sh"
echo "  3. Flatpak  : bash build_flatpak.sh"
echo ""
echo "📖 Documentation :"
echo "  • README.md           : Vue d'ensemble"
echo "  • UBUNTU_README.md    : Guide Ubuntu"
echo "  • FEDORA_README.md    : Guide Fedora/RPM/Flatpak"
echo "  • FLATPAK_README.md   : Guide détaillé Flatpak"
echo "  • MIGRATION_GUIDE.md  : Migration Debian → RPM/Flatpak"
echo "  • PROJECT_STRUCTURE.md: Structure complète du projet"
