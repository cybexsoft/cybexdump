#!/usr/bin/env bash

# Exit on error
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Error handler
trap 'printf "${RED}An error occurred during uninstallation. Please check the error message above.${NC}\n"' ERR

printf "${YELLOW}This will uninstall CybexDump and remove all configurations.${NC}\n"
read -p "Are you sure you want to continue? [y/N] " -n 1 -r
printf "\n"

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    printf "${GREEN}Uninstall cancelled.${NC}\n"
    exit 1
fi

# Function to safely remove a directory
safe_remove() {
    local dir=$1
    local desc=$2
    if [ -d "$dir" ]; then
        echo -e "${GREEN}Removing $desc...${NC}"
        rm -rf "$dir" || {
            echo -e "${RED}Failed to remove $desc at $dir${NC}"
            return 1
        }
    fi
}

# Function to clean up RC file
clean_rc_file() {
    local rc_file=$1
    local shell_name=$2
    if [ -f "$rc_file" ]; then
        echo -e "${GREEN}Cleaning up $shell_name configuration...${NC}"
        # Create backup
        cp "$rc_file" "${rc_file}.cybexdump.bak"
        # Remove cybexdump related lines
        sed -i '/cybexdump/d' "$rc_file" || {
            echo -e "${RED}Failed to clean $shell_name configuration. Restoring backup...${NC}"
            mv "${rc_file}.cybexdump.bak" "$rc_file"
            return 1
        }
        # Remove backup if successful
        rm "${rc_file}.cybexdump.bak"
    fi
}

# Remove virtual environment
safe_remove ~/.cybexdump-env "virtual environment"

# Remove configuration directory
safe_remove ~/.cybexdump "configuration files"

# Clean up shell configurations
clean_rc_file ~/.bashrc "bash"
clean_rc_file ~/.zshrc "zsh"

# Remove any pip cache for cybexdump
if [ -d ~/.cache/pip ]; then
    echo -e "${GREEN}Cleaning pip cache...${NC}"
    rm -rf ~/.cache/pip/cybexdump* 2>/dev/null || true
fi

printf "${GREEN}CybexDump has been successfully uninstalled!${NC}\n"
printf "${YELLOW}Please restart your shell for changes to take effect.${NC}\n"
