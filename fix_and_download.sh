#!/bin/bash
# Fix the download.sh path issue and download ModaNet images

# Get the package directory (adjust path if needed)
PYTHON_PKG_DIR="/c/Users/aliom/AppData/Roaming/Python/Python313/site-packages/maskrcnn_modanet"

# Check if package directory exists
if [ ! -d "$PYTHON_PKG_DIR" ]; then
    echo "ERROR: Package directory not found: $PYTHON_PKG_DIR"
    echo "Trying to find it..."
    # Try to find it using Python
    PYTHON_PKG_DIR=$(python -c "import maskrcnn_modanet; import os; print(os.path.dirname(maskrcnn_modanet.__file__))" 2>/dev/null | tr -d '\r')
    if [ -z "$PYTHON_PKG_DIR" ] || [ ! -d "$PYTHON_PKG_DIR" ]; then
        echo "Could not find package directory. Please check your Python installation."
        exit 1
    fi
    # Convert Windows path to Git Bash path
    PYTHON_PKG_DIR=$(echo "$PYTHON_PKG_DIR" | sed 's|\\|/|g' | sed 's|^C:|/c|')
fi

echo "Using package directory: $PYTHON_PKG_DIR"

# Check if download.sh exists
if [ ! -f "$PYTHON_PKG_DIR/download.sh" ]; then
    echo "ERROR: download.sh not found in package"
    exit 1
fi

echo "Found download.sh at: $PYTHON_PKG_DIR/download.sh"
echo ""

# Get current directory (project root)
PROJECT_DIR=$(pwd)
OUTPUT_DIR="$PROJECT_DIR/modanet_raw/images"

# Create output directory
mkdir -p "$OUTPUT_DIR"

echo "Output directory: $OUTPUT_DIR"
echo ""
echo "Running download script..."
echo "When prompted:"
echo "  - Type 'N' for 50k ModaNet images (recommended)"
echo "  - This will download ~55,000 images"
echo ""

# Change to the package directory and run the script
cd "$PYTHON_PKG_DIR"

# Run the download script
# The script expects: download.sh [output_path] [fast_download]
# fast_download=False means download full dataset
bash download.sh "$OUTPUT_DIR" "False"

