#!/bin/bash
# Wrapper Flatpak GUI pour auto-unlock-cryptnux
export XCURSOR_SIZE="${XCURSOR_SIZE:-24}"
export PYTHONPATH="/app/lib/auto-unlock-cryptnux:${PYTHONPATH}"
exec /app/bin/python3 /app/lib/auto-unlock-cryptnux/auto_unlock_cryptnux_gui.py "$@"
