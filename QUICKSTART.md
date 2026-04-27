# 🚀 Quick Start Guide - AutoUnlockCryptnux (Multi-Plateforme)

## Pour les utilisateurs impatients ⚡

### Ubuntu / Debian
```bash
# Installation depuis le paquet .deb
bash build_deb.sh
sudo dpkg -i auto-unlock-cryptnux_1.0.0_all.deb

# Utilisation
sudo auto-unlock-cryptnux-gui
```

### Fedora (RPM)
```bash
# Installation depuis RPM
bash build_rpm.sh
sudo dnf install ~/rpmbuild/RPMS/noarch/auto-unlock-cryptnux-*.noarch.rpm

# Utilisation
sudo auto-unlock-cryptnux-gui
```

### Flatpak (recommandé)
```bash
# Installation
sudo dnf install flatpak flatpak-builder      # Fedora
sudo apt install flatpak flatpak-builder      # Ubuntu/Debian

bash build_flatpak.sh
sudo flatpak install io.github.mentaldefeur.AutoUnlockCryptnux.flatpak

# Utilisation
flatpak run io.github.mentaldefeur.AutoUnlockCryptnux auto-unlock-cryptnux-gui
```

---

## Commandes essentielles

```bash
# Lister les partitions LUKS
sudo auto-unlock-cryptnux list

# Lier une partition au TPM2
sudo auto-unlock-cryptnux bind /dev/sda5

# Vérifier les dépendances
sudo auto-unlock-cryptnux check

# Interface graphique
sudo auto-unlock-cryptnux-gui
```

---

## 📖 Documentation complète

| Besoin | Lire |
|--------|------|
| Installation Ubuntu | [UBUNTU_README.md](UBUNTU_README.md) |
| Installation Fedora | [FEDORA_README.md](FEDORA_README.md) |
| Installation Flatpak | [FLATPAK_README.md](FLATPAK_README.md) |
| Technique (migrations) | [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) |
| Architecture complète | [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) |
| Détails changements | [TRANSFORMATION_COMPLETE.md](TRANSFORMATION_COMPLETE.md) |

---

## ⚙️ Dépannage rapide

```bash
# Vérifier la structure du projet
bash test_structure.sh

# Vérifier TPM2
ls /dev/tpm*

# Vérifier LUKS
sudo cryptsetup luksDump /dev/sda5

# Vérifier les permissions
sudo auto-unlock-cryptnux check
```

---

## 🎯 Objectif : Quelle distribution ?

- **Ubuntu/Debian** → `bash build_deb.sh`
- **Fedora** → `bash build_rpm.sh` OU `bash build_flatpak.sh`
- **Autre Linux** → `bash build_flatpak.sh`
- **Maximum portabilité** → Flatpak sur toutes les distros

---

## 📊 Comparaison rapide

| Aspect | Debian | RPM | Flatpak |
|--------|--------|-----|---------|
| Installation | `dpkg` | `dnf` | `flatpak` |
| Dépendances | Système | Système | Incluses |
| Portabilité | Ubuntu/Debian | Fedora/RHEL | Toutes |
| Taille | 5 MB | 5 MB | 200 MB |

---

## 🆘 Support

- Bug ? → https://github.com/MentalDeFeur/AutoUnlockCryptnux/issues
- Question ? → Lire la doc appropriée (`*_README.md`)
- Technique ? → Voir [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)

---

**Transformé le 27 avril 2026** ✨
