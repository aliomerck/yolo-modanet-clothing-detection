#!/bin/bash
# Script to download ModaNet images using Git Bash
# This script finds the maskrcnn-modanet executable and runs it

# Find the Python Scripts directory
PYTHON_SCRIPTS="$HOME/AppData/Roaming/Python/Python313/Scripts"

# Check if executable exists
if [ -f "$PYTHON_SCRIPTS/maskrcnn-modanet.exe" ]; then
    echo "Found maskrcnn-modanet at: $PYTHON_SCRIPTS/maskrcnn-modanet.exe"
    echo ""
    echo "Starting download..."
    echo "When prompted, type 'N' for 50k ModaNet images (recommended)"
    echo ""
    
    # Run the download command
    "$PYTHON_SCRIPTS/maskrcnn-modanet.exe" datasets download modanet_raw/images
else
    echo "ERROR: maskrcnn-modanet.exe not found at: $PYTHON_SCRIPTS/maskrcnn-modanet.exe"
    echo ""
    echo "Trying to find it in other locations..."
    
    # Try alternative locations
    ALTERNATIVE_LOCATIONS=(
        "/c/Users/$USER/AppData/Roaming/Python/Python313/Scripts"
        "/c/Users/$USER/AppData/Local/Programs/Python/Python313/Scripts"
        "/c/Python313/Scripts"
    )
    
    for loc in "${ALTERNATIVE_LOCATIONS[@]}"; do
        if [ -f "$loc/maskrcnn-modanet.exe" ]; then
            echo "Found at: $loc/maskrcnn-modanet.exe"
            "$loc/maskrcnn-modanet.exe" datasets download modanet_raw/images
            exit 0
        fi
    done
    
    echo ""
    echo "Could not find maskrcnn-modanet.exe"
    echo "Please run: pip install maskrcnn-modanet"
    echo "Then run this script again."
    exit 1
fi


