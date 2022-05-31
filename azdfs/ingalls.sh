#!/bin/sh
umount /Users/az/Code/azdfs/mount
exec poetry run python azdfs/main.py azdfs/ingalls.toml mount