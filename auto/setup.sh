#!/bin/bash

echo "Setting up Python project for macOS/Linux..."
echo

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
else
    OS="unknown"
fi

# Check Python
if command -v python3 &> /dev/null; then
    echo "Python found:"
    python3 --version
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    echo "Python found:"
    python --version
    PYTHON_CMD="python"
else
    echo "Python not found. Starting installation..."
    
    if [[ "$OS" == "macos" ]]; then
        # macOS - check Homebrew
        if command -v brew &> /dev/null; then
            echo "Installing Python via Homebrew..."
            brew install python
        else
            echo "Homebrew not found. Installing Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            echo "Installing Python..."
            brew install python
        fi
        PYTHON_CMD="python3"
        
    elif [[ "$OS" == "linux" ]]; then
        # Linux - detect distribution
        if command -v apt &> /dev/null; then
            echo "Installing Python via apt..."
            sudo apt update
            sudo apt install -y python3 python3-pip python3-venv
        elif command -v yum &> /dev/null; then
            echo "Installing Python via yum..."
            sudo yum install -y python3 python3-pip
        elif command -v dnf &> /dev/null; then
            echo "Installing Python via dnf..."
            sudo dnf install -y python3 python3-pip
        elif command -v pacman &> /dev/null; then
            echo "Installing Python via pacman..."
            sudo pacman -S python python-pip
        else
            echo "Package manager not supported. Please install Python manually."
            exit 1
        fi
        PYTHON_CMD="python3"
        
    else
        echo "OS not supported. Please install Python manually."
        exit 1
    fi
fi

# Verify Python installation
if ! command -v $PYTHON_CMD &> /dev/null; then
    echo "Python installation failed!"
    exit 1
fi

echo "Python installation verified:"
$PYTHON_CMD --version
echo

# Check pip
if ! $PYTHON_CMD -m pip --version &> /dev/null; then
    echo "Installing pip..."
    $PYTHON_CMD -m ensurepip --upgrade
    echo
fi

# Create virtual environment
if [ -d "venv" ]; then
    echo "Virtual environment already exists"
    echo
else
    echo "Creating virtual environment..."
    $PYTHON_CMD -m venv venv
    if [ $? -ne 0 ]; then
        echo "Error creating virtual environment!"
        exit 1
    fi
    echo "Virtual environment created successfully!"
    echo
fi

# Activate and install dependencies
echo "Activating virtual environment and installing dependencies..."
source venv/bin/activate

# Update pip
python -m pip install --upgrade pip

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
else
    echo "requirements.txt not found, skipping dependency installation"
fi

echo
echo "===== SETUP COMPLETED ====="
echo "To run the project use: ./run.sh"
echo "To activate environment use: source activate.sh"
echo

# Make other scripts executable
chmod +x run.sh 2>/dev/null
chmod +x activate.sh 2>/dev/null