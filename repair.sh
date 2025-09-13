#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting CybexDump repair...${NC}"

# Check if virtual environment exists
if [ ! -d ~/.cybexdump-env ]; then
    echo -e "${RED}Virtual environment not found. Please run install.sh first.${NC}"
    exit 1
fi

# Activate virtual environment
source ~/.cybexdump-env/bin/activate

# Get the package directory
PACKAGE_DIR=$(python3 -c "import os; import cybexdump; print(os.path.dirname(cybexdump.__file__))" 2>/dev/null || echo "")

if [ -z "$PACKAGE_DIR" ]; then
    echo -e "${YELLOW}Package not found in Python path. Attempting to fix...${NC}"
    
    # Try to find the installation
    if [ -d ~/cybexdump ]; then
        cd ~/cybexdump
    elif [ -d ./cybexdump ]; then
        cd .
    else
        echo -e "${RED}Could not find cybexdump installation directory.${NC}"
        exit 1
    fi

    # Ensure correct structure
    if [ ! -d cybexdump ]; then
        echo -e "${RED}Invalid package structure. Missing cybexdump directory.${NC}"
        exit 1
    fi

    # Reinstall package
    echo -e "${GREEN}Reinstalling package...${NC}"
    pip uninstall -y cybexdump
    pip install -e .

    # Verify installation
    python3 -c "from cybexdump.cli import cli" || {
        echo -e "${RED}Repair failed. Please try running install.sh again.${NC}"
        exit 1
    }
fi

echo -e "${GREEN}Package structure verified and fixed!${NC}"
echo -e "${YELLOW}You can now use 'cybexdump' command.${NC}"
