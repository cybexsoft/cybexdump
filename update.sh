#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting CybexDump Update...${NC}"

# Check if CybexDump is installed
if [ ! -d ~/.cybexdump-env ]; then
    echo -e "${RED}CybexDump is not installed. Please install it first.${NC}"
    exit 1
fi

# Create temporary directory
TMP_DIR=$(mktemp -d)
cd $TMP_DIR

# Backup current configuration
echo -e "${YELLOW}Backing up current configuration...${NC}"
if [ -d ~/.cybexdump ]; then
    cp -r ~/.cybexdump ./cybexdump_config_backup
fi

# Download latest version
echo -e "${GREEN}Downloading latest version...${NC}"
curl -L https://github.com/yourusername/cybexdump/archive/main.tar.gz -o cybexdump.tar.gz
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to download latest version.${NC}"
    exit 1
fi

# Extract package
tar xzf cybexdump.tar.gz
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to extract package.${NC}"
    exit 1
fi

# Activate virtual environment
source ~/.cybexdump-env/bin/activate

# Store current version
CURRENT_VERSION=$(cybexdump --version 2>/dev/null || echo "unknown")

# Install new version
cd cybexdump-main
echo -e "${GREEN}Installing updates...${NC}"
pip install --upgrade pip
pip install -e .

if [ $? -ne 0 ]; then
    echo -e "${RED}Update failed. Rolling back...${NC}"
    if [ -d ./cybexdump_config_backup ]; then
        rm -rf ~/.cybexdump
        mv ./cybexdump_config_backup ~/.cybexdump
    fi
    exit 1
fi

# Get new version
NEW_VERSION=$(cybexdump --version 2>/dev/null || echo "unknown")

# Restore configuration
if [ -d ./cybexdump_config_backup ]; then
    echo -e "${GREEN}Restoring configuration...${NC}"
    cp -r ./cybexdump_config_backup/* ~/.cybexdump/
fi

# Cleanup
cd
rm -rf $TMP_DIR

echo -e "${GREEN}CybexDump has been successfully updated!${NC}"
echo -e "${YELLOW}Previous version: ${CURRENT_VERSION}${NC}"
echo -e "${YELLOW}New version: ${NEW_VERSION}${NC}"

# Check if database clients need updating
echo -e "${YELLOW}Checking system dependencies...${NC}"

# Function to detect OS
detect_os() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$NAME
    elif type lsb_release >/dev/null 2>&1; then
        OS=$(lsb_release -si)
    elif [ -f /etc/lsb-release ]; then
        . /etc/lsb-release
        OS=$DISTRIB_ID
    else
        OS=$(uname -s)
    fi
}

# Update system dependencies based on OS
detect_os
case $OS in
    "Ubuntu"|"Debian")
        echo -e "${YELLOW}Updating system dependencies...${NC}"
        sudo apt-get update
        sudo apt-get upgrade -y mysql-client postgresql-client mongodb-clients
        ;;
    "CentOS"|"Red Hat"|"Fedora")
        echo -e "${YELLOW}Updating system dependencies...${NC}"
        sudo yum update -y mysql postgresql mongodb-org-shell
        ;;
    "macOS"|"Darwin")
        if command -v brew &> /dev/null; then
            echo -e "${YELLOW}Updating system dependencies using Homebrew...${NC}"
            brew upgrade mysql-client postgresql mongodb-community
        fi
        ;;
    *)
        echo -e "${YELLOW}Unknown OS. Please update MySQL, PostgreSQL, and MongoDB clients manually if needed.${NC}"
        ;;
esac

# Check for any new configuration options
echo -e "${YELLOW}Checking for new configuration options...${NC}"
cybexdump configure --check-updates

echo
echo -e "${GREEN}Update complete!${NC}"
echo -e "${YELLOW}To ensure all features work correctly, please restart your terminal or run:${NC}"
echo -e "source ~/.bashrc  # for bash"
echo -e "source ~/.zshrc   # for zsh"
