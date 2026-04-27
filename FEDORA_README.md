# Fedora - AutoUnlockCryptnux

Guide d'installation et de déploiement pour Fedora, avec support natif RPM et Flatpak.

## 📋 Prérequis

### Fedora (distribution native)
- Fedora 38+
- Python 3.8+
- TPM2 activé dans le BIOS/UEFI

```bash
ls /dev/tpm*  # Vérifier la présence du TPM2
```

### Flatpak (isolation complète)
- Fedora 33+
- Flatpak
- Runtime freedesktop 24.08

## 🛠️ Installation - Option 1 : Paquet RPM natif

### Prérequis de construction
```bash
sudo dnf install rpmdevtools fedora-packager python3-devel
```

### Construire le RPM
```bash
bash build_rpm.sh
```

### Installer le RPM
```bash
sudo dnf install ~/rpmbuild/RPMS/noarch/auto-unlock-cryptnux-*.noarch.rpm
```

### Vérifier l'installation
```bash
sudo auto-unlock-cryptnux check
```

## 📦 Installation - Option 2 : Flatpak

Flatpak est recommandé pour une isolation complète et une portabilité maximale.

### Prérequis
```bash
sudo dnf install flatpak flatpak-builder
sudo flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
sudo flatpak install flathub org.freedesktop.Platform//24.08 org.freedesktop.Sdk//24.08
```

### Construire et installer le Flatpak
```bash
bash build_flatpak.sh
sudo flatpak install io.github.mentaldefeur.AutoUnlockCryptnux.flatpak
```

Voir [FLATPAK_README.md](FLATPAK_README.md) pour plus de détails.

## 🚀 Utilisation

### Avec RPM natif
```bash
# Interface graphique
sudo auto-unlock-cryptnux-gui

# Ligne de commande
sudo auto-unlock-cryptnux list
sudo auto-unlock-cryptnux bind /dev/sda5
```

### Avec Flatpak
```bash
# Interface graphique
flatpak run io.github.mentaldefeur.AutoUnlockCryptnux auto-unlock-cryptnux-gui

# Ligne de commande
flatpak run io.github.mentaldefeur.AutoUnlockCryptnux auto-unlock-cryptnux list
flatpak run io.github.mentaldefeur.AutoUnlockCryptnux auto-unlock-cryptnux bind /dev/sda5
```

## 🔄 Déploiement sur COPR (Compile Obs Pour)

COPR permet de distribuer des RPM sur Fedora sans passage par le dépôt officiel.

### Prérequis
```bash
sudo dnf install copr-cli
```

### Configuration
```bash
# Obtenir un token sur https://copr.fedorainfracloud.org/
copr-cli config
```

### Créer un COPR
```bash
copr-cli create --chroot fedora-40-x86_64 auto-unlock-cryptnux
copr-cli create --chroot fedora-39-x86_64 auto-unlock-cryptnux
```

### Uploader le spec
```bash
copr-cli build auto-unlock-cryptnux auto-unlock-cryptnux.spec
```

### Installation depuis COPR
```bash
sudo dnf copr enable username/auto-unlock-cryptnux
sudo dnf install auto-unlock-cryptnux
```

## 📊 Comparaison : RPM vs Flatpak

| Aspect | RPM | Flatpak |
|--------|-----|---------|
| Intégration système | Excellente | Bonne (isolée) |
| Portabilité | Fedora seulement | Multi-distro |
| Taille | ~5 MB | ~200 MB |
| Dépendances système | Requises | Incluses |
| Accès TPM2 | Direct | Via mount/permissions |
| Startup | Rapide | +1-2s (démarrage runtime) |

**Recommandation :**
- **RPM** : Installation simple, intégration système native
- **Flatpak** : Meilleure portabilité, moins de conflits de dépendances

## 🐛 Dépannage Fedora

### Erreur : "clevis-luks not found"
```bash
sudo dnf install clevis clevis-luks clevis-tpm2
```

### Erreur : "TPM2 not detected"
Vérifier le BIOS/UEFI :
```bash
# Statut TPM2
systemctl status tpm2-abrmd  # Si TPM2 daemon est disponible
```

### Erreur : "Permission denied"
L'application a besoin de `sudo` ou `pkexec` :
```bash
pkexec auto-unlock-cryptnux-gui  # Via PolicyKit (recommandé)
# ou
sudo auto-unlock-cryptnux-gui    # Via sudo
```

### Erreur de permissions Flatpak TPM2
Vérifier les permissions Flatpak :
```bash
flatpak override io.github.mentaldefeur.AutoUnlockCryptnux --device=all
```

## 📝 Fichiers de configuration

```
/etc/crypttab              # Configuration du chiffrement (modifié par auto-unlock-cryptnux)
/etc/initramfs-tools/     # Configuration initramfs (pour clevis)
/boot/                     # Kernel et initrd
```

## 🔐 Sécurité

- L'application s'exécute en tant que root (via `sudo` ou `pkexec`)
- Les clés LUKS sont scellées dans le TPM2 (jamais stockées en clair)
- Intégrité vérifiée via les registres PCR (Secure Boot, firmware)
- Flatpak ajoute une couche d'isolation supplémentaire

## 📚 Ressources

- [Documentation Fedora](https://docs.fedoraproject.org/)
- [Guide RPM](https://rpm-packaging-guide.github.io/)
- [COPR Documentation](https://docs.pagure.org/copr.copr/)
- [Clevis Documentation](https://github.com/latchset/clevis)
- [TPM2 Documentation](https://github.com/tpm2-software/)
