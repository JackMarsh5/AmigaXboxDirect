#!/bin/bash
# entry.sh - Launch Amiga Xbox Direct Controller

cd /mnt/managed_home/farm-ng-user-jmarsh/amiga-xbox-direct
source venv/bin/activate
python3 -m amiga_xbox_direct.main
