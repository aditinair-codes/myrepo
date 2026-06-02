#!/bin/bash

# Change directory to current script directory
cd "$(dirname "$0")"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=======================================================================${NC}"
echo -e "${BLUE}         Setting Up Python Virtual Environment & Dependencies        ${NC}"
echo -e "${BLUE}=======================================================================${NC}"
echo ""

# Check and create virtual environment
if [ ! -d "venv" ]; then
    echo -e "${GREEN}[INFO] Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}[INFO] Virtual environment created successfully.${NC}"
else
    echo -e "${GREEN}[INFO] Virtual environment already exists.${NC}"
fi

# Activate virtual environment
echo -e "${GREEN}[INFO] Activating virtual environment...${NC}"
source venv/bin/activate

# Upgrade pip
echo -e "${GREEN}[INFO] Upgrading pip...${NC}"
python -m pip install --upgrade pip

# Install requirements
echo -e "${GREEN}[INFO] Installing requirements...${NC}"
python -m pip install -r ../../requirements.txt

echo ""
echo -e "${BLUE}=======================================================================${NC}"
echo -e "${GREEN}[SUCCESS] Setup completed! You can now run ./001_run.sh${NC}"
echo -e "${BLUE}=======================================================================${NC}"
