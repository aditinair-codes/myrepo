#!/bin/bash

# Change directory to current script directory
cd "$(dirname "$0")"

GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=======================================================================${NC}"
echo -e "${BLUE}             Starting Local Frontend Server (Inside Context)           ${NC}"
echo -e "${BLUE}=======================================================================${NC}"
echo ""

# Check virtual environment
if [ ! -d "venv" ]; then
    echo -e "${RED}[ERROR] Virtual environment not found!${NC}"
    echo -e "${GREEN}[INFO] Please run ./setup_env.sh first to set up the environment.${NC}"
    echo ""
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

echo -e "${GREEN}[INFO] Starting FastAPI server...${NC}"
python main.py
