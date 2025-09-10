#!/bin/bash

echo "Running Python project..."
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found!"
    echo "Please run ./setup.sh first"
    exit 1
fi

# Check if main.py exists
if [ ! -f "main.py" ]; then
    echo "main.py not found in project root!"
    exit 1
fi

# Activate virtual environment and run main.py
source venv/bin/activate
echo "Virtual environment activated"
echo "Running main.py..."
echo
python main.py

echo
echo "Program finished."