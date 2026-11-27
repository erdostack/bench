#!/bin/sh
set -eu
curl -sf "$PORTAL_URL/devices.json" -o /tmp/devices.json
python3 import/send.py import/import_devices.cypher /tmp/devices.json
