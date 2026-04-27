# Fedora + Flatpak - AutoUnlockCryptnux

Guide pour transformer ce projet en application Flatpak compatible avec Fedora.

## 📋 Prérequis

### Sur Fedora
```bash
sudo dnf install flatpak flatpak-builder
sudo flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
```

### Runtimes et SDK
```bash
sudo flatpak install flathub org.freedesktop.Platform//24.08
sudo flatpak install flathub org.freedesktop.Sdk//24.08
```

## 🔨 Construction

### Méthode 1 : Script automatique
```bash
bash build_flatpak.sh
```

### Méthode 2 : Commande flatpak-builder manuelle
```bash
flatpak-builder --repo=_flatpak_repo \
                --ccache \
                _flatpak_build \
                flatpak/io.github.mentaldefeur.AutoUnlockCryptnux.json
```

### Créer le bundle .flatpak
```bash
flatpak build-bundle _flatpak_repo \
                     io.github.mentaldefeur.AutoUnlockCryptnux.flatpak \
                     io.github.mentaldefeur.AutoUnlockCryptnux
```

## 📦 Installation

### Depuis le repository
```bash
flatpak install --user _flatpak_repo io.github.mentaldefeur.AutoUnlockCryptnux
```

### Depuis le bundle .flatpak
```bash
sudo flatpak install io.github.mentaldefeur.AutoUnlockCryptnux.flatpak
```

### Depuis Flathub (une fois publié)
```bash
sudo flatpak install flathub io.github.mentaldefeur.AutoUnlockCryptnux
```

## 🚀 Utilisation

### Interface graphique
```bash
flatpak run io.github.mentaldefeur.AutoUnlockCryptnux auto-unlock-cryptnux-gui
```

### Ligne de commande
```bash
# Lister les partitions LUKS
flatpak run io.github.mentaldefeur.AutoUnlockCryptnux auto-unlock-cryptnux list

# Lier une partition au TPM2
flatpak run io.github.mentaldefeur.AutoUnlockCryptnux auto-unlock-cryptnux bind /dev/sda5

# Vérifier les dépendances
flatpak run io.github.mentaldefeur.AutoUnlockCryptnux auto-unlock-cryptnux check
```

## 📋 Fichiers Flatpak

```
flatpak/
├── io.github.mentaldefeur.AutoUnlockCryptnux.json       # Manifeste Flatpak
├── io.github.mentaldefeur.AutoUnlockCryptnux.desktop    # Lanceur desktop
├── io.github.mentaldefeur.AutoUnlockCryptnux.metainfo.xml # Métadonnées AppData
├── wrapper-cli.sh                                     # Wrapper CLI
└── wrapper-gui.sh                                     # Wrapper GUI
```

## 🔧 Permissions (finish-args)

L'application a besoin des permissions suivantes :

- `--device=all` — Accès aux périphériques (TPM2)
- `--filesystem=host` — Accès au système de fichiers complet
- `--system-talk-name=org.freedesktop.DBus.System` — Communication D-Bus système
- `--socket=x11 --socket=wayland` — Interface graphique

## 📝 Déploiement sur Flathub

Pour publier sur [Flathub](https://flathub.org/) :

1. Fork https://github.com/flathub/flathub
2. Créer un PR avec :
   - `io.github.mentaldefeur.AutoUnlockCryptnux/` contenant :
     - `.github/workflows/` — CI/CD
     - `com.example.app.desktop`
     - `com.example.app.metainfo.xml`
     - `com.example.app.json` (manifeste)
   - `build-package.yml` pour la CI

Voir : https://docs.flathub.org/docs/for-app-authors/

## ⚙️ Alternatives et Optimisations

### Version légère (minimal)
Créer `io.github.mentaldefeur.AutoUnlockCryptnux-minimal.json` sans buildRequires externes :

```json
{
  "app-id": "io.github.mentaldefeur.AutoUnlockCryptnux",
  "modules": [
    {
      "name": "auto-unlock-cryptnux",
      "buildsystem": "simple",
      "build-commands": [
        "mkdir -p /app/bin /app/lib/auto-unlock-cryptnux",
        "cp auto_unlock_cryptnux*.py /app/lib/auto-unlock-cryptnux/",
        "cp flatpak/wrapper-*.sh /app/bin/"
      ]
    }
  ]
}
```

Cette version s'appuie sur les outils système (tpm2-tools, clevis, cryptsetup).

### Intégration RPM/Fedora

Pour une intégration native à Fedora (en plus de Flatpak) :

1. Créer `auto-unlock-cryptnux.spec` pour rpmbuild
2. Publier sur COPR : https://copr.fedorainfracloud.org/

## 🐛 Dépannage

### Erreur : "tpm2-tools not found"
Le Flatpak isole les outils. Vérifier que tpm2-tss est compilé correctement :
```bash
flatpak-builder --build-shell _flatpak_build \
                flatpak/io.github.mentaldefeur.AutoUnlockCryptnux.json
```

### Erreur : "PyQt5 not found"
L'extension Python3 du SDK doit être installée :
```bash
flatpak install org.freedesktop.Sdk.Extension.python3//24.08
```

### Accès TPM2 refusé
Vérifier les permissions :
```bash
ls -la /dev/tpm*
```

Le Flatpak a besoin de `--device=all` (déclaré dans finish-args).

## 📚 Ressources

- [Documentation Flatpak](https://docs.flatpak.org/)
- [Flathub Guidelines](https://docs.flathub.org/)
- [Flatpak Manifest Reference](https://docs.flatpak.org/en/latest/flatpak-manifest.html)
- [BuildRequires Best Practices](https://docs.flatpak.org/en/latest/manifests.html)
