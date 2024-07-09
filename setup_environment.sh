#!/bin/bash

# Path to your virtual environment
VENV_DIR="venv"

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv $VENV_DIR
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source $VENV_DIR/bin/activate

# Install requirements
if [ -f "requirements.txt" ]; then
    echo "Installing requirements..."
    pip3 install -r requirements.txt
else
    echo "requirements.txt not found. Please ensure it exists in the project root."
    exit 1
fi

echo "Setup complete."
