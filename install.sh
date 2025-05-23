#!/bin/bash
set -uxeo pipefail

# Resolve path to the current repo directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Create launcher manifest directory if it doesn't exist
mkdir -p ~/.farm-ng/manifest.d

# Link this app's manifest into the shared launcher directory
ln -sf "$DIR/manifest.json" ~/.farm-ng/manifest.d/amiga-xbox-direct.json

echo "✅ Linked manifest.json to ~/.farm-ng/manifest.d/amiga-xbox-direct.json"
