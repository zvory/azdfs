#!/bin/sh
umount /Users/az/Code/azdfs/mount
exec poetry run python -i azdfs/main.py azdfs/ingalls.toml mount