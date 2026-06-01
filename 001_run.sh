#!/bin/bash

# Title color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}=======================================================================${NC}"
echo -e "${GREEN}             Starting FirstStep.ai Designer Tool Server                ${NC}"
echo -e "${GREEN}=======================================================================${NC}"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo -e "${RED}[ERROR] Python 3 is not installed or not in PATH!${NC}"
    echo "Please install Python 3.8+ and try again."
    exit 1
fi

# Virtual env directory
VENV_DIR="applications/frontend/venv"

# Create venv if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${GREEN}[INFO] Creating Python virtual environment in ${VENV_DIR}...${NC}"
    python3 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        echo -e "${RED}[ERROR] Failed to create virtual environment!${NC}"
        exit 1
    fi
    echo -e "${GREEN}[INFO] Virtual environment created successfully.${NC}"
fi

# Activate virtual environment
echo -e "${GREEN}[INFO] Activating virtual environment...${NC}"
source "$VENV_DIR/bin/activate"

# Install dependencies
echo -e "${GREEN}[INFO] Upgrading pip and installing requirements...${NC}"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo -e "${RED}[ERROR] Failed to install requirements!${NC}"
    exit 1
fi

# Run the app
echo -e "${GREEN}[INFO] Starting FastAPI App...${NC}"
echo ""
python main.py
