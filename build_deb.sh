#!/bin/bash
# Construit le paquet .deb d'UbuntuTPM2Disk
set -e

PACKAGE="ubuntu-tpm2disk"
VERSION="1.0.0"
ARCH="all"
PKG_DIR="${PACKAGE}_${VERSION}_${ARCH}"

echo "=== Construction du paquet ${PKG_DIR}.deb ==="

# Nettoyer les anciennes constructions
rm -rf "$PKG_DIR" "${PKG_DIR}.deb"

# Créer la structure du paquet
mkdir -p "$PKG_DIR/DEBIAN"
mkdir -p "$PKG_DIR/usr/bin"
mkdir -p "$PKG_DIR/usr/lib/${PACKAGE}"
mkdir -p "$PKG_DIR/usr/share/applications"
mkdir -p "$PKG_DIR/usr/share/doc/${PACKAGE}"
mkdir -p "$PKG_DIR/usr/share/man/man1"

# --- DEBIAN/ ---
cp debian/control   "$PKG_DIR/DEBIAN/control"
cp debian/postinst  "$PKG_DIR/DEBIAN/postinst"
cp debian/prerm     "$PKG_DIR/DEBIAN/prerm"
chmod 755 "$PKG_DIR/DEBIAN/postinst" "$PKG_DIR/DEBIAN/prerm"

# --- Bibliothèque Python ---
cp ubuntu_tpm2disk.py      "$PKG_DIR/usr/lib/${PACKAGE}/ubuntu_tpm2disk.py"
cp ubuntu_tpm2disk_gui.py  "$PKG_DIR/usr/lib/${PACKAGE}/ubuntu_tpm2disk_gui.py"

# --- Wrappers exécutables ---
cat > "$PKG_DIR/usr/bin/ubuntu-tpm2disk" << 'WRAPPER'
#!/bin/bash
exec python3 /usr/lib/ubuntu-tpm2disk/ubuntu_tpm2disk.py "$@"
WRAPPER

cat > "$PKG_DIR/usr/bin/ubuntu-tpm2disk-gui" << 'WRAPPER'
#!/bin/bash
# Évite le conflit libpthread snap/core20 avec PyQt5 système
_SYS_PTHREAD=/usr/lib/x86_64-linux-gnu/libpthread.so.0
if [ -f "$_SYS_PTHREAD" ]; then
    export LD_PRELOAD="$_SYS_PTHREAD${LD_PRELOAD:+:$LD_PRELOAD}"
fi
exec python3 /usr/lib/ubuntu-tpm2disk/ubuntu_tpm2disk_gui.py "$@"
WRAPPER

chmod 755 "$PKG_DIR/usr/bin/ubuntu-tpm2disk" \
          "$PKG_DIR/usr/bin/ubuntu-tpm2disk-gui"

# --- Entrée .desktop ---
cat > "$PKG_DIR/usr/share/applications/ubuntu-tpm2disk.desktop" << 'DESKTOP'
[Desktop Entry]
Version=1.0
Type=Application
Name=UbuntuTPM2Disk
GenericName=Gestionnaire LUKS TPM2
Comment=Déverrouillage automatique des partitions LUKS via TPM2
Exec=pkexec ubuntu-tpm2disk-gui
Icon=drive-harddisk-encrypted
Terminal=false
Categories=System;Security;
Keywords=LUKS;TPM2;chiffrement;cryptsetup;
DESKTOP

# --- Documentation ---
cp README.md "$PKG_DIR/usr/share/doc/${PACKAGE}/README.md"
cp debian/copyright "$PKG_DIR/usr/share/doc/${PACKAGE}/copyright"

# Compresser le changelog
cp debian/changelog "$PKG_DIR/usr/share/doc/${PACKAGE}/changelog"
gzip -9 -n "$PKG_DIR/usr/share/doc/${PACKAGE}/changelog"

# --- Page de manuel ---
cat > "/tmp/${PACKAGE}.1" << 'MANPAGE'
.TH UBUNTU-TPM2DISK 1 "Avril 2026" "1.0.0" "UbuntuTPM2Disk"
.SH NOM
ubuntu-tpm2disk \- Gestionnaire de déverrouillage automatique LUKS via TPM2
.SH SYNOPSIS
.B ubuntu-tpm2disk
[\fICOMMANDE\fR] [\fIOPTIONS\fR]
.SH DESCRIPTION
Outil pour lier des partitions LUKS au module TPM2 matériel afin de permettre
un démarrage automatique sans saisie de mot de passe.
.SH COMMANDES
.TP
.B list
Lister les partitions LUKS et leur statut de liaison TPM2.
.TP
.B bind \fIPÉRIPHÉRIQUE\fR [\-\-pcr \fIIDS\fR]
Lier le périphérique LUKS au TPM2. PCR par défaut : 7 (Secure Boot).
.TP
.B unbind \fIPÉRIPHÉRIQUE\fR
Supprimer la liaison TPM2 du périphérique.
.TP
.B status
Afficher le statut du TPM2 et les valeurs PCR actuelles.
.TP
.B check
Vérifier les dépendances installées.
.SH EXEMPLES
.TP
Lier /dev/sda5 au TPM2 (PCR 7) :
.B sudo ubuntu-tpm2disk bind /dev/sda5
.TP
Lier avec plusieurs PCR :
.B sudo ubuntu-tpm2disk bind /dev/sda5 --pcr 0,1,7
.SH AUTEUR
UbuntuTPM2Disk Project
MANPAGE

gzip -9 -n -c "/tmp/${PACKAGE}.1" > "$PKG_DIR/usr/share/man/man1/${PACKAGE}.1.gz"
rm "/tmp/${PACKAGE}.1"

# --- md5sums ---
cd "$PKG_DIR"
find . -type f ! -path './DEBIAN/*' -exec md5sum {} \; \
    | sed 's|\./||' > DEBIAN/md5sums
cd ..

# --- Construire le .deb ---
dpkg-deb --build --root-owner-group "$PKG_DIR"

echo ""
echo "=== Paquet créé : ${PKG_DIR}.deb ==="
echo ""
echo "Installation :"
echo "  sudo dpkg -i ${PKG_DIR}.deb"
echo "  sudo apt-get install -f    # si des dépendances manquent"
echo ""

# Nettoyer le répertoire temporaire
rm -rf "$PKG_DIR"
