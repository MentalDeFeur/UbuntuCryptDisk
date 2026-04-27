# Migration Guide : Ubuntu → Fedora + Flatpak

Ce document explique les modifications apportées pour transformer le projet de format Debian (Ubuntu) en format RPM (Fedora) et Flatpak (multi-plateforme).

## 🔄 Changements majeurs

### 1. Structure des paquets

#### Ubuntu (.deb) - Ancienne approche
```
debian/                    # Métadonnées Debian
├── control              # Dépendances
├── postinst             # Script post-install
├── prerm                # Script pré-suppression
└── changelog            # Historique

build_deb.sh             # Script de construction
```

#### Fedora (RPM) - Nouvelle approche
```
auto-unlock-cryptnux.spec     # Spec RPM (tout-en-un)
build_rpm.sh             # Script de construction
```

#### Flatpak - Format universel
```
flatpak/                 # Manifeste et dépendances
├── *.json/.yaml         # Manifeste Flatpak
├── *.desktop            # Lanceur
└── *.metainfo.xml       # Métadonnées AppData
```

### 2. Gestion des dépendances

#### Ubuntu : Déclaratives (paquets système)
```bash
# Dans debian/control
Depends: python3 (>= 3.8), tpm2-tools, cryptsetup, python3-pyqt5
```

#### Fedora (RPM) : Déclaratives
```bash
# Dans auto-unlock-cryptnux.spec
Requires: tpm2-tools, cryptsetup, python3-pyqt5
```

#### Flatpak : Compilées dans le manifeste
```json
"modules": [
  {"name": "tpm2-tss", ...},
  {"name": "tpm2-tools", ...},
  {"name": "python3-pyqt5", ...}
]
```

**Avantage Flatpak :** Les dépendances sont **incluses** dans l'application (moins de conflits).

### 3. Scripts de construction

#### Avant : `build_deb.sh`
```bash
# Construction manuelle de la structure Debian
mkdir -p $PKG_DIR/DEBIAN
cp debian/control $PKG_DIR/DEBIAN/
cp auto_unlock_cryptnux.py $PKG_DIR/usr/lib/
chmod 755 $PKG_DIR/DEBIAN/postinst
dpkg-deb --build $PKG_DIR
```

#### RPM : `build_rpm.sh`
```bash
# Utilise rpmbuild (outil standard Fedora)
rpmdev-setuptree
tar -czf ~/rpmbuild/SOURCES/AutoUnlockCryptnux.tar.gz
rpmbuild -bb auto-unlock-cryptnux.spec
```

#### Flatpak : `build_flatpak.sh`
```bash
# Utilise flatpak-builder (outil standard Flatpak)
flatpak-builder _flatpak_build flatpak/manifest.json
flatpak build-bundle _flatpak_repo app.flatpak app-id
```

### 4. Métadonnées

#### Ubuntu : Fichiers séparés
- `debian/control` — Dépendances
- `debian/changelog` — Historique
- `debian/copyright` — Licence

#### RPM : Fichier unique
- `auto-unlock-cryptnux.spec` — Tout (dépendances, scripts, changelog)

#### Flatpak : Standard AppData
- `*.metainfo.xml` — Conforme [freedesktop.org AppData](https://www.freedesktop.org/software/appdata/)

### 5. Wrapper d'exécution

#### Ubuntu : Wrapper dans build_deb.sh
```bash
cat > /usr/bin/auto-unlock-cryptnux << 'EOF'
#!/bin/bash
exec python3 /usr/lib/auto-unlock-cryptnux/auto_unlock_cryptnux.py "$@"
EOF
```

#### Fedora (RPM) : Wrapper dans spec
```bash
cat > %{buildroot}%{_bindir}/auto-unlock-cryptnux << 'EOF'
#!/bin/bash
exec python3 %{python3_sitelib}/auto_unlock_cryptnux/auto_unlock_cryptnux.py "$@"
EOF
```

#### Flatpak : Wrapper dans flatpak/
```bash
# wrapper-cli.sh
exec /app/bin/python3 /app/lib/auto-unlock-cryptnux/auto_unlock_cryptnux.py "$@"
```

## 📋 Arborescence des répertoires

### Installation Ubuntu
```
/usr/bin/
├── auto-unlock-cryptnux           # Wrapper CLI
└── auto-unlock-cryptnux-gui       # Wrapper GUI

/usr/lib/auto-unlock-cryptnux/
├── auto_unlock_cryptnux.py
└── auto_unlock_cryptnux_gui.py

/usr/share/applications/
└── auto-unlock-cryptnux.desktop

/usr/share/doc/auto-unlock-cryptnux/
├── README.md
└── copyright
```

### Installation Fedora (RPM)
```
/usr/bin/
├── auto-unlock-cryptnux           # Wrapper CLI
└── auto-unlock-cryptnux-gui       # Wrapper GUI

/usr/lib/python3.*/site-packages/auto_unlock_cryptnux/
├── auto_unlock_cryptnux.py
└── auto_unlock_cryptnux_gui.py

/usr/share/applications/
└── auto-unlock-cryptnux.desktop

/usr/share/doc/auto-unlock-cryptnux/
└── README.md
```

### Installation Flatpak
```
/app/bin/
├── auto-unlock-cryptnux           # Wrapper CLI (flatpak/wrapper-cli.sh)
└── auto-unlock-cryptnux-gui       # Wrapper GUI (flatpak/wrapper-gui.sh)

/app/lib/auto-unlock-cryptnux/
├── auto_unlock_cryptnux.py
└── auto_unlock_cryptnux_gui.py

/app/bin/
├── tpm2_getcap              # (et autres outils tpm2)
└── cryptsetup

/app/share/applications/
└── io.github.mentaldefeur.AutoUnlockCryptnux.desktop

/app/share/metainfo/
└── io.github.mentaldefeur.AutoUnlockCryptnux.metainfo.xml
```

## 🔍 Comparaison des approches

| Aspect | Debian/Ubuntu | RPM/Fedora | Flatpak |
|--------|---------------|-----------|---------|
| **Format** | .deb | .rpm | .flatpak |
| **Outil** | dpkg/apt | dnf/rpm | flatpak |
| **Dépendances** | Système | Système | Intégrées |
| **Isolation** | Non | Non | Oui (sandbox) |
| **Taille** | ~5 MB | ~5 MB | ~200 MB |
| **Portabilité** | Ubuntu/Debian | Fedora/RHEL | Toute distro |
| **Mise à jour** | Système | Système | Auto (Flathub) |
| **Permissions** | root/dpkg | root/rpm | D-Bus/polkit |

## ✅ Checklist de migration

- [x] Créer `/flatpak/` avec manifeste JSON et YAML
- [x] Créer `auto-unlock-cryptnux.spec` pour RPM
- [x] Créer scripts `build_flatpak.sh` et `build_rpm.sh`
- [x] Adapter les chemins d'installation (site-packages vs lib)
- [x] Créer métadonnées AppData XML
- [x] Créer fichiers `.desktop` spécifiques
- [x] Documenter Fedora/Flatpak dans README
- [x] Tester construction RPM
- [x] Tester construction Flatpak
- [x] Mettre à jour `.gitignore`

## 🚀 Déploiement

### Ubuntu
```bash
# Sur Launchpad ou dans les repos PPAs
dput ppa:username/auto-unlock-cryptnux auto-unlock-cryptnux_*.changes
```

### Fedora
```bash
# Via COPR
copr-cli build auto-unlock-cryptnux auto-unlock-cryptnux.spec

# Ou directement sur repos Fedora (nécessite approbation)
fedpkg build
```

### Flatpak
```bash
# Sur Flathub
# Fork https://github.com/flathub/flathub
# PR vers flathub avec io.github.mentaldefeur.AutoUnlockCryptnux/
```

## 🐛 Points de compatibilité

### Chemins système
- **Ubuntu** : `/usr/lib/auto-unlock-cryptnux/`
- **Fedora** : `/usr/lib/python3.*/site-packages/auto_unlock_cryptnux/` ou `/usr/lib/auto-unlock-cryptnux/`
- **Flatpak** : `/app/lib/auto-unlock-cryptnux/`

**Solution :** Wrapper shellscript qui ajuste le chemin selon le contexte.

### Permissions
- **Ubuntu** : `sudo` ou `polkit` avec PolicyKit
- **Fedora** : Identique à Ubuntu
- **Flatpak** : `pkexec` via polkit dans le sandbox

### Dépendances manquantes
- **Ubuntu** : Vérifié via `Depends:` dans control
- **Fedora** : Vérifié via `Requires:` dans spec
- **Flatpak** : Incluses automatiquement

## 📚 Ressources

- [FPM - Flexible Package Manager](https://github.com/jordansissel/fpm) (outil multi-format)
- [Fedora Packaging Guidelines](https://docs.fedoraproject.org/en-US/packaging-guidelines/)
- [Flathub Documentation](https://docs.flathub.org/)
- [AppData Specification](https://www.freedesktop.org/software/appdata/)
