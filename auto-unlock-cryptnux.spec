Name:           auto-unlock-cryptnux
Version:        1.0.0
Release:        1%{?dist}
Summary:        Gestionnaire de déverrouillage automatique LUKS via TPM2
License:        MIT
URL:            https://github.com/MentalDeFeur/AutoUnlockCryptnux
Source0:        https://github.com/MentalDeFeur/AutoUnlockCryptnux/archive/main.tar.gz

BuildRequires:  python3-devel
BuildArch:      noarch

Requires:       python3 >= 3.8
Requires:       tpm2-tools
Requires:       cryptsetup
Requires:       util-linux
Requires:       python3-pyqt5
Requires:       clevis-luks
Recommends:     clevis-tpm2
Recommends:     clevis-initramfs

%description
Outil graphique et en ligne de commande pour lier des partitions LUKS chiffrées
au module TPM2 du matériel, permettant un démarrage automatique sans saisie
de mot de passe.

La clé LUKS est scellée dans le TPM2 et liée à des registres PCR (Platform
Configuration Registers). À chaque démarrage, si la configuration du système
correspond aux valeurs PCR enregistrées (Secure Boot actif, firmware inchangé…),
le TPM2 libère automatiquement la clé. En cas de modification suspecte,
le mot de passe LUKS reste requis.

%prep
%autosetup -n AutoUnlockCryptnux-main

%build
# Pas de compilation nécessaire pour du code Python pur

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{python3_sitelib}/auto_unlock_cryptnux
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_mandir}/man1

# Copier les modules Python
cp auto_unlock_cryptnux.py %{buildroot}%{python3_sitelib}/auto_unlock_cryptnux/auto_unlock_cryptnux.py
cp auto_unlock_cryptnux_gui.py %{buildroot}%{python3_sitelib}/auto_unlock_cryptnux/auto_unlock_cryptnux_gui.py

# Créer les wrappers exécutables
cat > %{buildroot}%{_bindir}/auto-unlock-cryptnux << 'EOF'
#!/bin/bash
exec python3 %{python3_sitelib}/auto_unlock_cryptnux/auto_unlock_cryptnux.py "$@"
EOF

cat > %{buildroot}%{_bindir}/auto-unlock-cryptnux-gui << 'EOF'
#!/bin/bash
exec python3 %{python3_sitelib}/auto_unlock_cryptnux/auto_unlock_cryptnux_gui.py "$@"
EOF

chmod 755 %{buildroot}%{_bindir}/auto-unlock-cryptnux \
          %{buildroot}%{_bindir}/auto-unlock-cryptnux-gui

# Créer l'entrée .desktop
cat > %{buildroot}%{_datadir}/applications/auto-unlock-cryptnux.desktop << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=AutoUnlockCryptnux
GenericName=Gestionnaire LUKS TPM2
Comment=Déverrouillage automatique des partitions LUKS via TPM2
Exec=pkexec auto-unlock-cryptnux-gui
Icon=drive-harddisk-encrypted
Terminal=false
Categories=System;Security;
Keywords=LUKS;TPM2;chiffrement;cryptsetup;
EOF

# Copier la documentation
cp README.md %{buildroot}%{_datadir}/doc/%{name}/README.md
cp debian/copyright %{buildroot}%{_datadir}/doc/%{name}/copyright

%files
%{_bindir}/auto-unlock-cryptnux
%{_bindir}/auto-unlock-cryptnux-gui
%{python3_sitelib}/auto_unlock_cryptnux/
%{_datadir}/applications/auto-unlock-cryptnux.desktop
%doc README.md

%post
systemctl daemon-reload || true
echo ""
echo "=== AutoUnlockCryptnux installé ==="
echo ""
echo "Commandes disponibles :"
echo "  sudo auto-unlock-cryptnux --help"
echo "  sudo auto-unlock-cryptnux-gui"
echo ""

%changelog
* Mon Apr 27 2026 AutoUnlockCryptnux Project <noreply@example.com> - 1.0.0-1
- Version initiale pour Fedora
- Support clevis-tpm2
- Support systemd-cryptenroll
- Interface graphique PyQt5
- Gestion PCR flexible
