#!/bin/bash
# Script de construction Flatpak pour AutoUnlockCryptnux (Fedora)
set -e

FLATPAK_ID="io.github.mentaldefeur.AutoUnlockCryptnux"
MANIFEST_FILE="flatpak/${FLATPAK_ID}.json"
BUILD_DIR="_flatpak_build"

echo "=== Construction Flatpak ${FLATPAK_ID} ==="

# Vérifier que les outils Flatpak sont installés
if ! command -v flatpak &> /dev/null; then
    echo "Flatpak n'est pas installé. Installez-le avec :"
    echo "  sudo dnf install flatpak flatpak-builder"
    exit 1
fi

if ! command -v flatpak-builder &> /dev/null; then
    echo "flatpak-builder n'est pas installé. Installez-le avec :"
    echo "  sudo dnf install flatpak-builder"
    exit 1
fi

# Nettoyer les anciennes constructions
if [ -d "$BUILD_DIR" ]; then
    echo "Nettoyage du répertoire de construction..."
    rm -rf "$BUILD_DIR"
fi

# Installer le runtime si nécessaire
echo "Vérification du runtime Flatpak..."
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo || true
for component in \
    org.freedesktop.Platform//24.08 \
    org.freedesktop.Sdk//24.08 \
    org.freedesktop.Sdk.Extension.python3//24.08; do
    if ! flatpak info "$component" &>/dev/null; then
        echo "Installation de $component..."
        flatpak install -y flathub "$component" || true
    fi
done

# Construire le Flatpak
# --share=network requis pour que pip puisse télécharger PyQt5 lors du build
echo "Construction en cours (réseau activé pour pip install PyQt5)..."
flatpak-builder --repo=_flatpak_repo \
                --ccache \
                --force-clean \
                --share=network \
                "$BUILD_DIR" \
                "$MANIFEST_FILE"

# Créer le bundle .flatpak
echo "Création du bundle Flatpak..."
flatpak build-bundle _flatpak_repo "${FLATPAK_ID}.flatpak" "${FLATPAK_ID}"

echo ""
echo "✓ Flatpak construit avec succès !"
echo ""
echo "Installation:"
echo "  sudo flatpak install ${FLATPAK_ID}.flatpak"
echo ""
echo "Exécution:"
echo "  flatpak run ${FLATPAK_ID}"
echo ""
echo "Lancement du GUI:"
echo "  flatpak run ${FLATPAK_ID} auto-unlock-cryptnux-gui"
echo ""
