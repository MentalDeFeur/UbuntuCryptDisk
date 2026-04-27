#!/usr/bin/env python3
"""
AutoUnlockCryptnux - Déverrouillage automatique LUKS via TPM2
Lie des partitions LUKS chiffrées au module TPM2 pour un démarrage
sans saisie de mot de passe. Supporte clevis-tpm2 et systemd-cryptenroll.
"""

import sys
import os
import subprocess
import json
import shutil
import argparse
from pathlib import Path


# ---------------------------------------------------------------------------
# Détection système
# ---------------------------------------------------------------------------

def check_root():
    if os.geteuid() != 0:
        print("Ce programme doit être exécuté en tant que root: sudo auto-unlock-cryptnux")
        sys.exit(1)


def get_tpm2_backend():
    """Retourne 'clevis' | 'systemd-cryptenroll' | None"""
    if shutil.which('clevis'):
        return 'clevis'
    if shutil.which('systemd-cryptenroll'):
        return 'systemd-cryptenroll'
    return None


def check_dependencies():
    """Retourne la liste des paquets manquants."""
    missing = []
    if not shutil.which('tpm2_getcap'):
        missing.append('tpm2-tools')
    if not shutil.which('cryptsetup'):
        missing.append('cryptsetup')
    if not shutil.which('lsblk'):
        missing.append('util-linux')
    if get_tpm2_backend() is None:
        missing.append('clevis-luks (ou systemd 248+ pour systemd-cryptenroll)')
    return missing


def check_tpm2_available():
    """Retourne (bool, chemin_device|None). Vérifie l'existence du device sans l'ouvrir."""
    for dev in ('/dev/tpmrm0', '/dev/tpm0'):
        if Path(dev).exists():
            return True, dev
    return False, None


# ---------------------------------------------------------------------------
# Détection des partitions LUKS
# ---------------------------------------------------------------------------

def get_luks_devices():
    """Retourne la liste des périphériques LUKS (fermés et ouverts)."""
    try:
        r = subprocess.run(
            ['lsblk', '-o', 'NAME,TYPE,FSTYPE,SIZE,MOUNTPOINT', '-J'],
            capture_output=True, text=True, check=True
        )
        data = json.loads(r.stdout)
        devices = []

        def scan(devlist):
            for dev in devlist:
                if dev.get('fstype') == 'crypto_LUKS':
                    devices.append({
                        'name': dev['name'],
                        'device': f"/dev/{dev['name']}",
                        'size': dev.get('size', ''),
                        'status': 'fermé',
                    })
                elif dev.get('type') == 'crypt':
                    devices.append({
                        'name': dev['name'],
                        'device': f"/dev/mapper/{dev['name']}",
                        'size': dev.get('size', ''),
                        'status': 'ouvert',
                        'mountpoint': dev.get('mountpoint') or '',
                    })
                if 'children' in dev:
                    scan(dev['children'])

        scan(data.get('blockdevices', []))
        return devices
    except Exception as e:
        print(f"Erreur détection partitions: {e}", file=sys.stderr)
        return []


# ---------------------------------------------------------------------------
# Statut de liaison TPM2
# ---------------------------------------------------------------------------

def get_tpm2_binding_status(device):
    """Retourne (bool_lié, description)."""
    if os.geteuid() != 0:
        return False, "(root requis pour vérifier)"
    backend = get_tpm2_backend()
    if backend == 'clevis':
        try:
            r = subprocess.run(
                ['clevis', 'luks', 'list', '-d', device],
                capture_output=True, text=True, timeout=5
            )
            if r.returncode == 0 and 'tpm2' in r.stdout:
                return True, r.stdout.strip()
        except Exception as e:
            return False, str(e)
    elif backend == 'systemd-cryptenroll':
        try:
            r = subprocess.run(
                ['systemd-cryptenroll', device],
                capture_output=True, text=True, timeout=5
            )
            if r.returncode == 0 and 'tpm2' in r.stdout.lower():
                return True, r.stdout.strip()
        except Exception as e:
            return False, str(e)
    return False, "non lié"


# ---------------------------------------------------------------------------
# Liaison LUKS → TPM2
# ---------------------------------------------------------------------------

def bind_luks_to_tpm2(device, pcr_ids='7'):
    """
    Lie le périphérique LUKS au TPM2 en utilisant le backend disponible.
    Demande le mot de passe LUKS de manière interactive.
    Retourne (bool, message).
    """
    backend = get_tpm2_backend()
    if backend is None:
        return False, "Aucun backend TPM2 disponible (installez clevis-luks ou systemd 248+)"

    if backend == 'clevis':
        pcr_cfg = json.dumps({"pcr_ids": pcr_ids}) if pcr_ids else '{}'
        print(f"  Méthode : clevis-tpm2  (PCR : {pcr_ids})")
        print("  Entrez le mot de passe LUKS actuel :")
        try:
            r = subprocess.run(
                ['clevis', 'luks', 'bind', '-d', device, 'tpm2', pcr_cfg],
                timeout=120
            )
            if r.returncode == 0:
                return True, "Liaison clevis-tpm2 réussie"
            return False, f"clevis a échoué (code {r.returncode})"
        except subprocess.TimeoutExpired:
            return False, "Timeout"
        except Exception as e:
            return False, str(e)

    # systemd-cryptenroll
    print(f"  Méthode : systemd-cryptenroll  (PCR : {pcr_ids})")
    print("  Entrez le mot de passe LUKS actuel :")
    cmd = ['systemd-cryptenroll', '--tpm2-device=auto', device]
    if pcr_ids:
        cmd.append(f'--tpm2-pcrs={pcr_ids}')
    try:
        r = subprocess.run(cmd, timeout=120)
        if r.returncode == 0:
            return True, "Liaison systemd-cryptenroll réussie"
        return False, f"systemd-cryptenroll a échoué (code {r.returncode})"
    except subprocess.TimeoutExpired:
        return False, "Timeout"
    except Exception as e:
        return False, str(e)


# ---------------------------------------------------------------------------
# Suppression de la liaison
# ---------------------------------------------------------------------------

def unbind_luks_from_tpm2(device):
    """Supprime la liaison TPM2 du périphérique LUKS. Retourne (bool, message)."""
    backend = get_tpm2_backend()

    if backend == 'clevis':
        try:
            r = subprocess.run(
                ['clevis', 'luks', 'list', '-d', device],
                capture_output=True, text=True, timeout=5
            )
            for line in r.stdout.splitlines():
                if 'tpm2' in line:
                    slot = line.split(':')[0].strip()
                    subprocess.run(
                        ['clevis', 'luks', 'unlink', '-d', device, '-s', slot],
                        check=True, timeout=10
                    )
            return True, "Liaison TPM2 supprimée"
        except Exception as e:
            return False, str(e)

    if backend == 'systemd-cryptenroll':
        try:
            r = subprocess.run(
                ['systemd-cryptenroll', '--wipe-slot=tpm2', device],
                timeout=30
            )
            if r.returncode == 0:
                return True, "Liaison TPM2 supprimée"
            return False, f"Erreur (code {r.returncode})"
        except Exception as e:
            return False, str(e)

    return False, "Aucun backend disponible"


# ---------------------------------------------------------------------------
# /etc/crypttab
# ---------------------------------------------------------------------------

def configure_crypttab_tpm2(device, mapping_name):
    """Ajoute ou met à jour l'entrée crypttab pour le déverrouillage TPM2."""
    backend = get_tpm2_backend()
    if backend == 'clevis':
        options = 'luks,discard,clevis'
    elif backend == 'systemd-cryptenroll':
        options = 'luks,discard,tpm2-device=auto'
    else:
        return False, "Aucun backend disponible"

    line = f"{mapping_name} {device} none {options}\n"
    crypttab = Path('/etc/crypttab')

    lines = crypttab.read_text().splitlines(keepends=True) if crypttab.exists() else []
    updated = False
    new_lines = []
    for l in lines:
        parts = l.split()
        if parts and parts[0] == mapping_name:
            new_lines.append(line)
            updated = True
        else:
            new_lines.append(l)
    if not updated:
        new_lines.append(line)

    crypttab.write_text(''.join(new_lines))
    return True, f"crypttab : {line.strip()}"


def update_initramfs():
    """Régénère l'initramfs pour inclure la configuration TPM2."""
    backend = get_tpm2_backend()
    if backend == 'clevis':
        # S'assurer que clevis-initramfs est présent
        hooks = Path('/usr/share/initramfs-tools/hooks/clevis')
        if not hooks.exists():
            print("  Installation de clevis-initramfs...")
            subprocess.run(['apt', 'install', '-y', 'clevis-initramfs'], check=True)

    r = subprocess.run(['update-initramfs', '-u', '-k', 'all'],
                       capture_output=True, text=True)
    return r.returncode == 0


# ---------------------------------------------------------------------------
# PCR
# ---------------------------------------------------------------------------

def get_pcr_values(pcr_list='0,1,2,3,4,5,6,7'):
    if os.geteuid() != 0:
        return "(droits root requis — lancez avec sudo ou ajoutez votre user au groupe tss)"
    try:
        r = subprocess.run(
            ['tpm2_pcrread', f'sha256:{pcr_list}'],
            capture_output=True, text=True, check=True, timeout=10
        )
        return r.stdout
    except subprocess.CalledProcessError as e:
        stderr = e.stderr or ''
        if 'Permission denied' in stderr or 'access denied' in stderr.lower():
            return "(permission refusée — ajoutez votre user au groupe tss : sudo usermod -aG tss $USER)"
        return f"Erreur tpm2_pcrread : {stderr.strip() or e}"
    except Exception as e:
        return f"Erreur lecture PCR : {e}"


# ---------------------------------------------------------------------------
# Sous-commandes
# ---------------------------------------------------------------------------

def cmd_list(args):
    print("=== Partitions LUKS ===\n")
    devices = get_luks_devices()
    if not devices:
        print("Aucune partition LUKS trouvée.")
        return 0
    for dev in devices:
        print(f"  {dev['device']}  ({dev['size']})  [{dev['status']}]")
        if dev['status'] == 'fermé':
            bound, info = get_tpm2_binding_status(dev['device'])
            if bound:
                print(f"    TPM2 : LIE AU TPM2")
                print(f"    Info : {info}")
            else:
                print(f"    TPM2 : {info}")
        else:
            mp = dev.get('mountpoint', '')
            if mp:
                print(f"    Monté : {mp}")
        print()
    return 0


def cmd_bind(args):
    check_root()
    device = args.device
    pcr_ids = args.pcr or '7'

    print(f"=== Liaison TPM2 : {device} ===\n")

    if not Path(device).exists():
        print(f"Erreur : le périphérique {device} n'existe pas.")
        return 1

    available, tpm_dev = check_tpm2_available()
    if not available:
        print("Erreur : aucun module TPM2 détecté.")
        print("Vérifiez que le TPM2 est activé dans le BIOS/UEFI.")
        return 1

    print(f"TPM2 : {tpm_dev}")
    print(f"PCR  : {pcr_ids}\n")

    ok, msg = bind_luks_to_tpm2(device, pcr_ids)
    if not ok:
        print(f"\nEchec : {msg}")
        return 1

    print(f"\nSuccès : {msg}")

    mapping = f"luks_{Path(device).name.replace('-', '_')}"
    ok2, msg2 = configure_crypttab_tpm2(device, mapping)
    print(f"crypttab : {'OK' if ok2 else 'ERREUR - ' + msg2}")

    print("initramfs : mise à jour en cours...")
    if update_initramfs():
        print("initramfs : OK")
    else:
        print("initramfs : ERREUR (vérifiez avec update-initramfs -u)")

    print(f"\n{device} se déverrouillera automatiquement au prochain démarrage.")
    return 0


def cmd_unbind(args):
    check_root()
    device = args.device
    print(f"=== Suppression liaison TPM2 : {device} ===\n")
    ok, msg = unbind_luks_from_tpm2(device)
    if ok:
        print(f"Succès : {msg}")
        print("Pensez à mettre à jour /etc/crypttab si nécessaire.")
    else:
        print(f"Echec : {msg}")
    return 0 if ok else 1


def cmd_status(args):
    print("=== Statut TPM2 ===\n")
    available, tpm_dev = check_tpm2_available()
    backend = get_tpm2_backend()
    print(f"TPM2 hardware : {'Oui (' + tpm_dev + ')' if available else 'Non détecté'}")
    print(f"Backend       : {backend or 'Aucun'}")
    if available:
        print("\nValeurs PCR sha256 :")
        print(get_pcr_values())
    return 0


def cmd_check(args):
    print("=== Vérification des dépendances ===\n")
    tools = {
        'tpm2_getcap (tpm2-tools)': shutil.which('tpm2_getcap'),
        'cryptsetup': shutil.which('cryptsetup'),
        'lsblk': shutil.which('lsblk'),
        'clevis': shutil.which('clevis'),
        'systemd-cryptenroll': shutil.which('systemd-cryptenroll'),
        'update-initramfs': shutil.which('update-initramfs'),
    }
    for name, path in tools.items():
        print(f"  {'OK' if path else 'MANQUANT':<10} {name}")

    missing = check_dependencies()
    if missing:
        print("\nInstallation des manquants :")
        print("  sudo apt install tpm2-tools clevis-luks clevis-tpm2 clevis-initramfs")
    else:
        print("\nToutes les dépendances sont présentes.")

    available, tpm_dev = check_tpm2_available()
    print(f"\nHardware TPM2 : {'Détecté (' + tpm_dev + ')' if available else 'Non détecté'}")
    return 0 if not missing else 1


# ---------------------------------------------------------------------------
# Menu interactif
# ---------------------------------------------------------------------------

def interactive_menu():
    while True:
        print("\n=== AutoUnlockCryptnux ===")
        print("  1. Lister les partitions LUKS")
        print("  2. Lier une partition au TPM2")
        print("  3. Supprimer une liaison TPM2")
        print("  4. Statut TPM2 & PCR")
        print("  5. Vérifier les dépendances")
        print("  0. Quitter")

        choice = input("\nChoix : ").strip()

        class A:
            device = None
            pcr = '7'

        if choice == '0':
            break
        elif choice == '1':
            cmd_list(A())
        elif choice == '2':
            a = A()
            a.device = input("Périphérique (ex: /dev/sda5) : ").strip()
            a.pcr = input("PCR IDs [7] : ").strip() or '7'
            cmd_bind(a)
        elif choice == '3':
            a = A()
            a.device = input("Périphérique (ex: /dev/sda5) : ").strip()
            cmd_unbind(a)
        elif choice == '4':
            cmd_status(A())
        elif choice == '5':
            cmd_check(A())


# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        prog='auto-unlock-cryptnux',
        description='Déverrouillage automatique LUKS via TPM2'
    )
    sub = parser.add_subparsers(dest='command')

    sub.add_parser('list', help='Lister les partitions LUKS').set_defaults(func=cmd_list)

    p_bind = sub.add_parser('bind', help='Lier une partition LUKS au TPM2')
    p_bind.add_argument('device', help='Ex: /dev/sda5')
    p_bind.add_argument('--pcr', default='7',
                        help='PCR IDs à utiliser (défaut: 7). Ex: 0,1,7')
    p_bind.set_defaults(func=cmd_bind)

    p_unbind = sub.add_parser('unbind', help='Supprimer la liaison TPM2')
    p_unbind.add_argument('device', help='Ex: /dev/sda5')
    p_unbind.set_defaults(func=cmd_unbind)

    sub.add_parser('status', help='Statut TPM2 et valeurs PCR').set_defaults(func=cmd_status)
    sub.add_parser('check', help='Vérifier les dépendances').set_defaults(func=cmd_check)

    args = parser.parse_args()
    if args.command is None:
        interactive_menu()
        return 0
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
