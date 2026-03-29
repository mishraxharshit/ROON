#!/bin/bash
# macOS / Linux launcher
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ ! -d "venv" ]; then
    echo "Setting up for first time..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt --quiet
    python3 generate_icon.py
else
    source venv/bin/activate
fi

python3 pdf_reader.py "$@"
deactivate
