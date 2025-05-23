#!/bin/bash
set -e

# Set up virtual environment
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi
source venv/bin/activate

# Upgrade pip and install Python dependencies
pip install --upgrade pip
pip install -e .

# Build frontend if present
if [ -d "ts" ]; then
  echo "Building frontend..."
  cd ts/
  npm install
  npm run build
  cd ..
fi

# Final status
echo "✅ Bootstrap complete. Activate the environment with: source venv/bin/activate"
