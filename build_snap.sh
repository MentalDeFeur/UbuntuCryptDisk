#!/bin/bash
# Script de construction Snap pour AutoUnlockCryptnux
set -e

SNAP_NAME="auto-unlock-cryptnux_1.0.0_amd64.snap"

echo "=== Construction du paquet Snap pour AutoUnlockCryptnux ==="
echo ""

# Vérifier que snapcraft est installé
if ! command -v snapcraft &> /dev/null; then
    echo "snapcraft n'est pas installé."
    echo ""
    echo "Installation sur Ubuntu/Debian :"
    echo "  sudo snap install snapcraft --classic"
    echo ""
    echo "Installation sur Fedora :"
    echo "  sudo dnf install snapd"
    echo "  sudo systemctl enable --now snapd.socket"
    echo "  sudo ln -s /var/lib/snapd/snap /snap"
    echo "  sudo snap install snapcraft --classic"
    echo ""
    echo "Alternative via LXD (recommandé sur Fedora) :"
    echo "  snapcraft --use-lxd"
    exit 1
fi

# Construire le snap
echo "Construction en cours (confinement : classic)..."
echo "Le build se fait dans un conteneur LXD ou Multipass."
echo ""

# --destructive-mode : build directement sur le système hôte (Ubuntu seulement)
# --use-lxd         : build dans un conteneur LXD
if snapcraft --destructive-mode 2>/dev/null; then
    true
else
    echo "Tentative avec LXD..."
    snapcraft --use-lxd
fi

# Afficher le résultat
if ls *.snap 1>/dev/null 2>&1; then
    echo ""
    echo "Snap construit avec succès !"
    echo ""
    echo "Fichier créé :"
    ls -lh *.snap
    echo ""
    echo "Installation :"
    echo "  sudo snap install *.snap --classic --dangerous"
    echo ""
    echo "Exécution :"
    echo "  sudo auto-unlock-cryptnux --help"
    echo "  sudo auto-unlock-cryptnux-gui"
    echo ""
else
    echo "Erreur : aucun fichier .snap trouvé"
    exit 1
fi
