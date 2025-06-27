#!/bin/bash

VENV_DIR=".venv"
REQUIREMENTS_FILE="requirements.txt"

# 💡 Offer to rebuild the environment
offer_rebuild() {
    echo ""
    echo "⚠️  The virtual environment appears to be incomplete or broken."
    read -p "❓ Do you want to delete and rebuild it now? (y/N) " choice
    case "$choice" in
        y|Y )
            echo "🧹 Deleting existing virtual environment..."
            rm -rf "$VENV_DIR"
            echo "🔁 Restarting setup..."
            exec "$0" "$@"  # Re-run with same arguments
            ;;
        * )
            echo ""
            echo "👉 To install manually:"
            echo "   source $VENV_DIR/bin/activate"
            echo "   pip install -r $REQUIREMENTS_FILE"
            echo ""
            echo "🔁 Or re-run './run.sh' and select 'y' when prompted."
            exit 1
            ;;
    esac
}

# 💡 Offer to install requirements if missing
offer_install_requirements() {
    echo ""
    echo "⚠️  Some required packages are not installed in the virtual environment."
    read -p "❓ Install missing dependencies now? (y/N) " choice
    case "$choice" in
        y|Y )
            echo "📦 Installing dependencies from $REQUIREMENTS_FILE..."
            echo " Checking if pip is up to date..."
            python -m pip install --upgrade pip
            if pip install -r "$REQUIREMENTS_FILE"; then
                echo "✅ Dependencies installed."
            else
                echo "❌ Installation failed."
                offer_rebuild "$@"
            fi
            ;;
        * )
            echo ""
            echo "👉 To install manually:"
            echo "   source $VENV_DIR/bin/activate"
            echo "   pip install -r $REQUIREMENTS_FILE"
            echo ""
            echo "🔁 Or re-run './run.sh' and select 'y' when prompted."
            exit 1
            ;;
    esac
}

# Step 1: Create venv if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv "$VENV_DIR" || exit 1
fi

# Step 2: Activate venv
source "$VENV_DIR/bin/activate"

# Step 3: Check for missing packages from requirements.txt
missing=0
while read -r req; do
    # Skip comments and empty lines
    [[ "$req" =~ ^#.*$ || -z "$req" ]] && continue
    # Extract package name (ignore extras and version)
    pkg=$(echo "$req" | sed -E 's/([<=>].*)?$//' | cut -d'[' -f1)
    pip show "$pkg" > /dev/null 2>&1 || missing=1
done < "$REQUIREMENTS_FILE"

if [ "$missing" -eq 1 ]; then
    offer_install_requirements "$@"
fi

# Step 4: Run your main Python program with any args passed
python main.py "$@"