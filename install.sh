#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting CybexDump Installation...${NC}"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3 first.${NC}"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
if (( $(echo "$PYTHON_VERSION < 3.7" | bc -l) )); then
    echo -e "${RED}Python 3.7 or higher is required. Current version: $PYTHON_VERSION${NC}"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo -e "${YELLOW}Installing pip...${NC}"
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py --user
    rm get-pip.py
fi

# Create temporary directory
TMP_DIR=$(mktemp -d)
cd $TMP_DIR

# Clone the repository or download the package
echo -e "${GREEN}Downloading CybexDump...${NC}"
curl -L https://github.com/yourusername/cybexdump/archive/main.tar.gz -o cybexdump.tar.gz
tar xzf cybexdump.tar.gz

# Navigate to the package directory
cd cybexdump-main

# Install required system packages
echo -e "${GREEN}Checking system requirements...${NC}"

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

# Install system dependencies based on OS
detect_os
case $OS in
    "Ubuntu"|"Debian")
        echo -e "${YELLOW}Installing system dependencies...${NC}"
        sudo apt-get update
        sudo apt-get install -y mysql-client postgresql-client mongodb-clients
        ;;
    "CentOS"|"Red Hat"|"Fedora")
        echo -e "${YELLOW}Installing system dependencies...${NC}"
        sudo yum install -y mysql postgresql mongodb-org-shell
        ;;
    "macOS"|"Darwin")
        if command -v brew &> /dev/null; then
            echo -e "${YELLOW}Installing system dependencies using Homebrew...${NC}"
            brew install mysql-client postgresql mongodb-community
        else
            echo -e "${RED}Homebrew is not installed. Please install Homebrew first.${NC}"
            exit 1
        fi
        ;;
    *)
        echo -e "${YELLOW}Unknown OS. Please install MySQL, PostgreSQL, and MongoDB clients manually if needed.${NC}"
        ;;
esac

# Create virtual environment
echo -e "${GREEN}Creating virtual environment...${NC}"
python3 -m venv ~/.cybexdump-env

# Activate virtual environment
source ~/.cybexdump-env/bin/activate

# Install Python dependencies
echo -e "${GREEN}Installing Python dependencies...${NC}"
pip install --upgrade pip
pip install -e .

# Create configuration directory
mkdir -p ~/.cybexdump

# Create shell completion
echo -e "${GREEN}Setting up shell completion...${NC}"
SHELL_RC=""
if [ -n "$BASH_VERSION" ]; then
    SHELL_RC="$HOME/.bashrc"
elif [ -n "$ZSH_VERSION" ]; then
    SHELL_RC="$HOME/.zshrc"
fi

if [ -n "$SHELL_RC" ]; then
    echo 'eval "$(_CYBEXDUMP_COMPLETE=bash_source cybexdump)"' >> "$SHELL_RC"
    echo "export PATH=\$PATH:\$HOME/.cybexdump-env/bin" >> "$SHELL_RC"
fi

# Cleanup
cd
rm -rf $TMP_DIR

echo -e "${GREEN}CybexDump has been successfully installed!${NC}"
echo -e "${YELLOW}Please restart your shell or run:${NC}"
echo -e "${YELLOW}source $SHELL_RC${NC}"
echo
echo -e "${GREEN}You can start using CybexDump by running:${NC}"
echo -e "cybexdump --help"
echo
echo -e "${YELLOW}To configure CybexDump, run:${NC}"
echo -e "cybexdump configure"
