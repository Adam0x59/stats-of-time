#!/bin/bash

# Path to venv
VENV_DIR=".venv"

# Check if venv exists
if [ ! -d "$VENV_DIR" ]; then
    echo "🔧 Virtual environment not found. Setting it up..."
    python3 -m venv $VENV_DIR
    source $VENV_DIR/bin/activate
    echo "📦 Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
else
    source $VENV_DIR/bin/activate
fi

# Run your main script
python main.py