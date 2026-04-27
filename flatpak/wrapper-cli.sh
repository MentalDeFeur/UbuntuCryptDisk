#!/bin/bash
export PYTHONPATH="/app/lib/python3.12/site-packages:${PYTHONPATH}"
exec python3 /app/lib/auto-unlock-cryptnux/auto_unlock_cryptnux.py "$@"
