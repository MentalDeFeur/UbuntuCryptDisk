# 📚 INDEX - Documentation du projet AutoUnlockCryptnux (Fedora + Flatpak)

## 🎯 Par où commencer ?

### Si tu viens de découvrir le projet
👉 Lire en premier : [QUICKSTART.md](QUICKSTART.md)

### Si tu veux installer
- Ubuntu/Debian ? → [UBUNTU_README.md](UBUNTU_README.md)
- Fedora ? → [FEDORA_README.md](FEDORA_README.md)
- N'importe où ? → [FLATPAK_README.md](FLATPAK_README.md)

### Si tu veux comprendre les détails techniques
👉 [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) — Explique pourquoi et comment ça a changé

### Si tu veux voir la structure complète
👉 [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) — Arborescence et organisation

---

## 📋 Fichiers de documentation

| Fichier | Audience | Résumé |
|---------|----------|--------|
| **QUICKSTART.md** | Tous | Commandes rapides pour installer |
| **README.md** | Tous | Vue d'ensemble et guide général |
| **UBUNTU_README.md** | Ubuntu/Debian | Installation .deb depuis sources |
| **FEDORA_README.md** | Fedora | Installation RPM ou Flatpak + COPR |
| **FLATPAK_README.md** | Flatpak | Construction et déploiement Flatpak |
| **MIGRATION_GUIDE.md** | Développeurs | Détails techniques des migrations |
| **PROJECT_STRUCTURE.md** | Développeurs | Arborescence et organization |
| **TRANSFORMATION_COMPLETE.md** | Développeurs | Synthèse complète des changements |
| **INDEX.md** | Tous | Ce fichier |

---

## 🔨 Fichiers de construction

| Fichier | Plateforme | Usage |
|---------|-----------|-------|
| `build_deb.sh` | Ubuntu/Debian | `bash build_deb.sh` → `.deb` |
| `build_rpm.sh` | Fedora | `bash build_rpm.sh` → `.rpm` |
| `build_flatpak.sh` | Multi-plateforme | `bash build_flatpak.sh` → `.flatpak` |
| `test_structure.sh` | Tous | `bash test_structure.sh` → Validation |

---

## 🎯 Fichiers de configuration

### Debian/Ubuntu
```
debian/
├── control        # Dépendances (.deb)
├── changelog      # Historique versions
├── postinst       # Script post-installation
├── prerm          # Script pré-suppression
└── ...
```

### Fedora (RPM)
```
auto-unlock-cryptnux.spec  # Spec RPM (tout-en-un)
```

### Flatpak
```
flatpak/
├── io.github.mentaldefeur.AutoUnlockCryptnux.json     # Manifeste (JSON)
├── io.github.mentaldefeur.AutoUnlockCryptnux.yaml     # Manifeste (YAML)
├── io.github.mentaldefeur.AutoUnlockCryptnux.desktop  # Lanceur
├── io.github.mentaldefeur.AutoUnlockCryptnux.metainfo.xml  # Métadonnées
├── wrapper-cli.sh     # Wrapper CLI
└── wrapper-gui.sh     # Wrapper GUI
```

---

## 💻 Commandes rapides

### Construction
```bash
# Ubuntu
bash build_deb.sh

# Fedora (RPM)
bash build_rpm.sh

# Flatpak
bash build_flatpak.sh

# Validation
bash test_structure.sh
```

### Installation
```bash
# Ubuntu
sudo dpkg -i auto-unlock-cryptnux_1.0.0_all.deb

# Fedora (RPM)
sudo dnf install ~/rpmbuild/RPMS/noarch/auto-unlock-cryptnux-*.rpm

# Flatpak
sudo flatpak install io.github.mentaldefeur.AutoUnlockCryptnux.flatpak
```

### Utilisation
```bash
# CLI
sudo auto-unlock-cryptnux list
sudo auto-unlock-cryptnux bind /dev/sda5

# GUI
sudo auto-unlock-cryptnux-gui          # Ubuntu/Fedora (RPM)
flatpak run io.github.mentaldefeur.AutoUnlockCryptnux auto-unlock-cryptnux-gui  # Flatpak
```

---

## 🗂️ Structure des répertoires

```
AutoUnlockCryptnux/
│
├── 📄 README.md                    # Guide principal
├── 📄 QUICKSTART.md                # Guide de démarrage rapide
├── 📄 UBUNTU_README.md             # Guide Ubuntu
├── 📄 FEDORA_README.md             # Guide Fedora
├── 📄 FLATPAK_README.md            # Guide Flatpak
├── 📄 MIGRATION_GUIDE.md           # Détails techniques
├── 📄 PROJECT_STRUCTURE.md         # Architecture
├── 📄 TRANSFORMATION_COMPLETE.md   # Synthèse changements
├── 📄 INDEX.md                     # Ce fichier
│
├── 🐍 auto_unlock_cryptnux.py           # Module CLI
├── 🐍 auto_unlock_cryptnux_gui.py       # Module GUI
│
├── 🔨 build_deb.sh                 # Construction Debian/Ubuntu
├── 🔨 build_rpm.sh                 # Construction Fedora RPM
├── 🔨 build_flatpak.sh             # Construction Flatpak
├── 🔨 test_structure.sh            # Validation structure
│
├── 🎯 auto-unlock-cryptnux.spec         # Spec RPM
│
├── 📁 debian/                      # Métadonnées Debian/Ubuntu
│   └── control, changelog, ...
│
├── 📁 flatpak/                     # Configuration Flatpak
│   ├── *.json, *.yaml              # Manifestes
│   ├── *.desktop, *.xml            # Métadonnées/Lanceurs
│   └── wrapper-*.sh                # Wrappers
│
├── 📁 docs/                        # Documentation et ressources
│   └── screenshot.png
│
├── .git/                           # Repository Git
├── .gitignore                      # Fichiers ignorés
└── README.md                       # Vue d'ensemble (modifié)
```

---

## ✅ Points de contrôle

- [x] Structure Flatpak créée
- [x] Spec RPM créée
- [x] Scripts de construction opérationnels
- [x] Documentation complète
- [x] JSON Flatpak validé
- [x] Tests de structure passés
- [x] .gitignore mis à jour

---

## 🚀 Prochaines étapes (optionnelles)

### Publication
- [ ] Flathub (https://flathub.org/)
- [ ] COPR Fedora (https://copr.fedorainfracloud.org/)
- [ ] PPA Ubuntu (Launchpad)

### Automatisation
- [ ] CI/CD GitHub Actions
- [ ] Signature GPG des paquets
- [ ] Tests de construction automatiques

---

## 🔗 Ressources externes

### Documentation
- [Flatpak Docs](https://docs.flatpak.org/)
- [RPM Packaging](https://rpm-packaging-guide.github.io/)
- [Debian Packaging](https://www.debian.org/doc/debian-policy/)

### Outils
- [Flathub Developer](https://docs.flathub.org/docs/for-app-authors/)
- [COPR](https://copr.fedorainfracloud.org/)
- [Fedora Build System](https://docs.fedoraproject.org/en-US/package-maintainers/)

---

## 📞 Support

- 🐛 Bug report : https://github.com/MentalDeFeur/AutoUnlockCryptnux/issues
- 💬 Discussion : https://github.com/MentalDeFeur/AutoUnlockCryptnux/discussions
- 📖 Docs : Voir fichiers `*_README.md`

---

**Dernière mise à jour : 27 avril 2026**
