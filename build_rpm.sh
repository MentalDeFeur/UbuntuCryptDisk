#!/bin/bash
# Script de construction RPM pour AutoUnlockCryptnux sur Fedora
set -e

echo "=== Construction du paquet RPM pour Fedora ==="

# Vérifier que rpmbuild est installé
if ! command -v rpmbuild &> /dev/null; then
    echo "❌ rpmbuild n'est pas installé. Installez-le avec:"
    echo "   sudo dnf install rpmdevtools fedora-packager"
    exit 1
fi

# Initialiser la structure RPM si nécessaire
RPMTOP="$HOME/rpmbuild"
if [ ! -d "$RPMTOP" ]; then
    echo "Initialisation de la structure RPM..."
    rpmdev-setuptree
fi

# Récupérer la version
VERSION=$(grep -oP "Version:\s*\K[0-9.]+(?=\s|$)" auto-unlock-cryptnux.spec)
TARBALL="AutoUnlockCryptnux-${VERSION}.tar.gz"

# Créer la source
echo "Création de l'archive source..."
git archive --format tar.gz --output "$RPMTOP/SOURCES/$TARBALL" HEAD 2>/dev/null || \
    tar --exclude=.git --exclude=_build --exclude=_flatpak_* \
        -czf "$RPMTOP/SOURCES/$TARBALL" \
        --transform='s,^,AutoUnlockCryptnux-'"${VERSION}"'/,' \
        $(ls -A | grep -v '^_')

# Construire le RPM
echo "Construction du RPM..."
rpmbuild -bb auto-unlock-cryptnux.spec

# Afficher le résultat
RPM_FILE="$RPMTOP/RPMS/noarch/auto-unlock-cryptnux-${VERSION}-1.fc*.noarch.rpm"
if ls $RPM_FILE 1> /dev/null 2>&1; then
    echo ""
    echo "✓ RPM construit avec succès !"
    echo ""
    echo "Fichier créé :"
    ls -lh $RPM_FILE
    echo ""
    echo "Installation :"
    echo "  sudo dnf install $RPM_FILE"
    echo ""
else
    echo "❌ Erreur : Impossible de trouver le RPM généré"
    exit 1
fi
