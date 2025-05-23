#!/bin/bash
set -uxeo pipefail

# Get full path to this repo
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Create launcher manifest directory if it doesn't exist
mkdir -p ~/.farm-ng/manifest.d

# Symlink this app's manifest.json into the shared directory
ln -sf "$DIR/manifest.json" ~/.farm-ng/manifest.d/amiga-xbox-direct.json
