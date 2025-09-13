#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}This will uninstall CybexDump and remove all configurations.${NC}"
read -p "Are you sure you want to continue? [y/N] " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo -e "${GREEN}Uninstall cancelled.${NC}"
    exit 1
fi

# Remove virtual environment
if [ -d ~/.cybexdump-env ]; then
    echo -e "${GREEN}Removing virtual environment...${NC}"
    rm -rf ~/.cybexdump-env
fi

# Remove configuration directory
if [ -d ~/.cybexdump ]; then
    echo -e "${GREEN}Removing configuration files...${NC}"
    rm -rf ~/.cybexdump
fi

# Remove shell completion and PATH from shell RC files
if [ -f ~/.bashrc ]; then
    echo -e "${GREEN}Cleaning up bash configuration...${NC}"
    sed -i '/cybexdump/d' ~/.bashrc
fi

if [ -f ~/.zshrc ]; then
    echo -e "${GREEN}Cleaning up zsh configuration...${NC}"
    sed -i '/cybexdump/d' ~/.zshrc
fi

echo -e "${GREEN}CybexDump has been successfully uninstalled!${NC}"
echo -e "${YELLOW}Please restart your shell for changes to take effect.${NC}"
