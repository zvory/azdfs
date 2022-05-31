#!/bin/sh
umount mount0
exec poetry run python -i azdfs/main.py azdfs/config0.toml mount0