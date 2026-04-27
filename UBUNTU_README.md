# Ubuntu - AutoUnlockCryptnux

Guide d'installation pour Ubuntu 20.04+.

## 📋 Prérequis

- Ubuntu 20.04 ou supérieur
- TPM2 activé dans le BIOS/UEFI (`/dev/tpm0` ou `/dev/tpmrm0` présent)
- Secure Boot recommandé (PCR 7)

### Vérifier la présence du TPM2
```bash
ls /dev/tpm*
```

## 🛠️ Installation

### Via le paquet .deb

```bash
# Télécharger la dernière release puis :
sudo dpkg -i auto-unlock-cryptnux_1.0.0_all.deb
sudo apt-get install -f          # installe les dépendances manquantes
```

### Depuis les sources

```bash
git clone https://github.com/MentalDeFeur/AutoUnlockCryptnux.git
cd AutoUnlockCryptnux

# Dépendances (backend clevis)
sudo apt install tpm2-tools cryptsetup python3-pyqt5 \
                 clevis-luks clevis-tpm2 clevis-initramfs

# Ou avec systemd-cryptenroll (Ubuntu 22.04+)
sudo apt install tpm2-tools cryptsetup python3-pyqt5

# Construire le .deb
bash build_deb.sh
sudo dpkg -i auto-unlock-cryptnux_1.0.0_all.deb
```

## 🚀 Utilisation

### Interface graphique

```bash
sudo auto-unlock-cryptnux-gui
```

### Ligne de commande

```bash
# Lister les partitions LUKS et leur statut TPM2
sudo auto-unlock-cryptnux list

# Lier une partition au TPM2 (PCR 7 = Secure Boot, recommandé)
sudo auto-unlock-cryptnux bind /dev/sda5

# Lier avec plusieurs PCR
sudo auto-unlock-cryptnux bind /dev/sda5 --pcr 0,1,7

# Supprimer la liaison TPM2
sudo auto-unlock-cryptnux unbind /dev/sda5

# Statut TPM2 et valeurs PCR actuelles
sudo auto-unlock-cryptnux status

# Vérifier les dépendances
sudo auto-unlock-cryptnux check

# Menu interactif
sudo auto-unlock-cryptnux
```

## 🔄 Mise à jour

```bash
sudo apt update
sudo apt upgrade
```

## 🗑️ Désinstallation

```bash
sudo apt remove auto-unlock-cryptnux
```

## 🆘 Dépannage

### Erreur : "clevis-luks not found"
```bash
sudo apt install clevis clevis-luks clevis-tpm2 clevis-initramfs
```

### Erreur : "TPM2 not detected"
```bash
# Vérifier le BIOS/UEFI (doit être activé)
# Recharger le module kernel
sudo modprobe -r tpm_tis
sudo modprobe tpm_tis
```

### Partition LUKS non détectée
```bash
# Lister les partitions chiffrées
sudo cryptsetup luksDump /dev/sda5
```

## 📚 Ressources

- [Documentation Clevis](https://github.com/latchset/clevis)
- [Documentation TPM2](https://github.com/tpm2-software/)
- [Ubuntu SecurityGuide - LUKS](https://wiki.ubuntu.com/SecurityTeam/Luks/)
