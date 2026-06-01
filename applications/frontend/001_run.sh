#!/bin/bash

# Change directory to current script directory
cd "$(dirname "$0")"

GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}=======================================================================${NC}"
echo -e "${GREEN}             Starting Local Frontend Server (Inside Context)           ${NC}"
echo -e "${GREEN}=======================================================================${NC}"
echo ""

# Check virtual environment
if [ ! -d "venv" ]; then
    echo -e "${GREEN}[INFO] No virtual environment found. Creating...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    python -m pip install --upgrade pip
    python -m pip install -r ../../requirements.txt
else
    source venv/bin/activate
fi

python main.py
