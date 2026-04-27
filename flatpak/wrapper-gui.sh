#!/bin/bash
export PYTHONPATH="/app/lib/python3.12/site-packages:${PYTHONPATH}"
export XCURSOR_SIZE="${XCURSOR_SIZE:-24}"
exec python3 /app/lib/auto-unlock-cryptnux/auto_unlock_cryptnux_gui.py "$@"
