#!/bin/bash
# Wrapper Flatpak CLI pour auto-unlock-cryptnux
exec /app/bin/python3 /app/lib/auto-unlock-cryptnux/auto_unlock_cryptnux.py "$@"
