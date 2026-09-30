#!/bin/bash
# Script to help set up wget and tar for Git Bash

echo "Checking for required tools..."
echo ""

# Check for wget
if command -v wget &> /dev/null; then
    echo "✓ wget is installed: $(which wget)"
else
    echo "✗ wget is NOT installed"
    echo ""
    echo "Installing wget..."
    
    # Try pacman (MSYS2)
    if command -v pacman &> /dev/null; then
        echo "Using pacman to install wget..."
        pacman -S --noconfirm wget
    else
        echo "pacman not available. Please install wget manually:"
        echo "1. Download from: https://eternallybored.org/misc/wget/"
        echo "2. Extract wget.exe to: C:/Program Files/Git/usr/bin/"
        echo ""
        echo "Or add wget directory to your PATH"
    fi
fi

# Check for tar
if command -v tar &> /dev/null; then
    echo "✓ tar is installed: $(which tar)"
else
    echo "✗ tar is NOT installed"
    echo "tar should come with Git Bash. If missing, reinstall Git for Windows"
fi

# Check for git-lfs
if command -v git-lfs &> /dev/null; then
    echo "✓ git-lfs is installed: $(which git-lfs)"
else
    echo "✗ git-lfs is NOT installed"
    echo "Installing git-lfs..."
    if command -v pacman &> /dev/null; then
        pacman -S --noconfirm git-lfs
    else
        echo "Please install Git LFS: https://git-lfs.github.com/"
    fi
fi

echo ""
echo "Setup complete!"
echo ""
echo "To verify, run:"
echo "  wget --version"
echo "  tar --version"
echo "  git lfs version"


