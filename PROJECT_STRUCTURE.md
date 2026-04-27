# 📁 Structure du projet - AutoUnlockCryptnux

```
AutoUnlockCryptnux/
│
├── 📄 README.md                          # Guide principal (multi-plateforme)
├── 📄 UBUNTU_README.md                   # Guide Ubuntu spécifique
├── 📄 FEDORA_README.md                   # Guide Fedora/RPM/Flatpak
├── 📄 FLATPAK_README.md                  # Guide détaillé Flatpak
│
├── 🐍 auto_unlock_cryptnux.py                 # Module CLI principal
├── 🐍 auto_unlock_cryptnux_gui.py             # Module GUI (PyQt5)
│
├── 🔨 build_deb.sh                       # Construction paquet Debian/Ubuntu
├── 🔨 build_rpm.sh                       # Construction paquet Fedora RPM
├── 🔨 build_flatpak.sh                   # Construction Flatpak
│
├── 🎯 auto-unlock-cryptnux.spec               # Spec RPM pour Fedora
│
├── 📁 debian/                            # Métadonnées Debian/Ubuntu
│   ├── changelog                         # Historique versions
│   ├── compat                            # Version compatibilité debhelper
│   ├── control                           # Dépendances et métadonnées
│   ├── copyright                         # License et droits d'auteur
│   ├── postinst                          # Script post-installation
│   └── prerm                             # Script pré-suppression
│
├── 📁 flatpak/                           # Configuration Flatpak
│   ├── io.github.mentaldefeur.AutoUnlockCryptnux.json
│   │                                    # Manifeste Flatpak (JSON)
│   ├── io.github.mentaldefeur.AutoUnlockCryptnux.yaml
│   │                                    # Manifeste Flatpak (YAML alternative)
│   ├── io.github.mentaldefeur.AutoUnlockCryptnux.desktop
│   │                                    # Entrée lanceur desktop
│   ├── io.github.mentaldefeur.AutoUnlockCryptnux.metainfo.xml
│   │                                    # Métadonnées AppData
│   ├── wrapper-cli.sh                    # Wrapper CLI Flatpak
│   └── wrapper-gui.sh                    # Wrapper GUI Flatpak
│
├── 📁 docs/                              # Documentation et ressources
│   └── screenshot.png                    # Capture d'écran GUI
│
├── .git/                                 # Repository Git
├── .gitignore                            # Fichiers ignorés Git
│
└── 📄 MIGRATION_GUIDE.md                 # Guide migration Ubuntu → Fedora

```

## 📊 Format de distribution

| Format | Plateforme | Fichier | Outil |
|--------|-----------|---------|-------|
| **DEB** | Ubuntu/Debian | `*.deb` | `dpkg` / `apt` |
| **RPM** | Fedora/RHEL | `*.rpm` | `dnf` / `rpm` |
| **Flatpak** | Multi-distro | `*.flatpak` | `flatpak` |

## 🔄 Flux de construction

### Ubuntu (.deb)
```
auto_unlock_cryptnux*.py → build_deb.sh → debian/ → .deb
```

### Fedora (RPM)
```
auto_unlock_cryptnux*.py → build_rpm.sh → auto-unlock-cryptnux.spec → .rpm
```

### Flatpak
```
auto_unlock_cryptnux*.py → flatpak/ → build_flatpak.sh → .flatpak
```

## 📝 Documentation

| Fichier | Audience | Contenu |
|---------|----------|---------|
| `README.md` | Tous les utilisateurs | Vue d'ensemble et guide de démarrage rapide |
| `UBUNTU_README.md` | Utilisateurs Ubuntu | Installation .deb et sources |
| `FEDORA_README.md` | Utilisateurs Fedora | Installation RPM et COPR |
| `FLATPAK_README.md` | Utilisateurs Flatpak | Construction et déploiement Flatpak |
| `MIGRATION_GUIDE.md` | Développeurs | Migration de Ubuntu vers Fedora |

## 🎯 Points d'entrée

### Ubuntu
- `sudo auto-unlock-cryptnux-gui` (GUI)
- `sudo auto-unlock-cryptnux` (CLI interactif)
- `sudo auto-unlock-cryptnux bind /dev/sda5` (CLI direct)

### Fedora (RPM)
- Identique à Ubuntu (même binaire)

### Fedora/Multi-distro (Flatpak)
- `flatpak run io.github.mentaldefeur.AutoUnlockCryptnux auto-unlock-cryptnux-gui`
- `flatpak run io.github.mentaldefeur.AutoUnlockCryptnux auto-unlock-cryptnux`

## 🚀 Prochaines étapes

1. **Publication Flathub**
   - Créer PR sur https://github.com/flathub/flathub
   - Manifeste dans `io.github.mentaldefeur.AutoUnlockCryptnux/`

2. **Publication COPR (Fedora)**
   - Créer compte sur https://copr.fedorainfracloud.org/
   - `copr-cli build auto-unlock-cryptnux auto-unlock-cryptnux.spec`

3. **Publication Ubuntu PPA**
   - Créer clé GPG
   - Configurer PPA sur Launchpad
   - `dput ppa:username/auto-unlock-cryptnux auto-unlock-cryptnux_*.changes`

## 🔐 Sécurité

- ✅ Clés LUKS scellées dans TPM2 (jamais en clair)
- ✅ Intégrité vérifiée via PCR (Secure Boot, firmware)
- ✅ Root/polkit requis (protection par permissions)
- ✅ Flatpak ajoute isolation additionnelle
