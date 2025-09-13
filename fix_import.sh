#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Fixing CybexDump installation...${NC}"

# Check if virtual environment exists
if [ ! -d ~/.cybexdump-env ]; then
    echo -e "${RED}Virtual environment not found at ~/.cybexdump-env${NC}"
    exit 1
fi

# Activate virtual environment
source ~/.cybexdump-env/bin/activate

# Create a temporary fix script
cat > /tmp/fix_cybexdump.py << 'EOL'
#!/usr/bin/env python3
import sys
import os

def main():
    print("Debug: Current sys.path =", sys.path)
    print("Debug: Looking for cybexdump package...")
    
    try:
        import cybexdump
        print("Debug: Found cybexdump at:", cybexdump.__file__)
    except ImportError as e:
        print("Debug: Import error:", e)
        return 1

    try:
        from cybexdump.cli import cli
        print("Debug: Successfully imported cli")
        return 0
    except ImportError as e:
        print("Debug: CLI import error:", e)
        return 1

if __name__ == '__main__':
    sys.exit(main())
EOL

# Run the fix script
python3 /tmp/fix_cybexdump.py

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Package import check successful.${NC}"
else
    echo -e "${RED}Package import check failed.${NC}"
    echo -e "${YELLOW}Attempting to fix...${NC}"
    
    # Remove old installation
    pip uninstall -y cybexdump
    
    # Get the actual package directory
    PACKAGE_DIR=$(dirname $(dirname $0))
    cd "$PACKAGE_DIR"
    
    # Install in editable mode with explicit path
    PYTHONPATH="$PWD" pip install -e .
    
    # Verify fix
    python3 /tmp/fix_cybexdump.py
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Fix successful!${NC}"
    else
        echo -e "${RED}Fix failed. Please run install.sh again.${NC}"
        exit 1
    fi
fi

# Clean up
rm -f /tmp/fix_cybexdump.py

echo -e "${GREEN}Fix completed. Try using 'cybexdump' command now.${NC}"
