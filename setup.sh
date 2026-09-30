#!/bin/bash
# Quick setup script for YOLOv11 ModaNet project

echo "=========================================="
echo "YOLOv11 ModaNet Setup Script"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Check if Git LFS is installed
echo ""
echo "Checking Git LFS installation..."
if command -v git-lfs &> /dev/null; then
    echo "✓ Git LFS is installed"
    git lfs install
else
    echo "✗ Git LFS is not installed"
    echo "Please install Git LFS:"
    echo "  macOS: brew install git-lfs"
    echo "  Linux: sudo apt-get install git-lfs"
    echo "  Windows: Download from https://git-lfs.github.com/"
    exit 1
fi

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Download ModaNet annotations:"
echo "   python download_modanet.py"
echo ""
echo "2. Download ModaNet images (see README.md for instructions)"
echo ""
echo "3. Convert to YOLO format:"
echo "   python convert_modanet_to_yolo.py \\"
echo "     --train-json modanet_raw/modanet2018_instances_train.json \\"
echo "     --val-json modanet_raw/modanet2018_instances_val.json \\"
echo "     --images-dir modanet_raw/images \\"
echo "     --output-dir modanet_yolo"
echo ""
echo "4. Train the model:"
echo "   python train_yolo.py --data modanet_yolo/modanet.yaml --model l"


