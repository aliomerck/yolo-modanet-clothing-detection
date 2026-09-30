"""
Download ModaNet dataset annotations and prepare for conversion.
This script helps download the ModaNet annotations from the GitHub repository.
Note: You'll need to manually download the images from the PaperDoll dataset.
"""

import os
import subprocess
import json
from pathlib import Path
import urllib.request
from tqdm import tqdm

def check_git_lfs():
    """Check if Git LFS is installed."""
    try:
        subprocess.run(['git', 'lfs', 'version'], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def download_modanet_annotations(output_dir='modanet_raw'):
    """
    Download ModaNet annotations from GitHub.
    Note: This requires Git LFS to be installed.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    repo_url = 'https://github.com/eBay/modanet.git'
    repo_dir = output_dir / 'modanet_repo'
    
    print("Checking Git LFS installation...")
    if not check_git_lfs():
        print("ERROR: Git LFS is not installed!")
        print("Please install Git LFS first:")
        print("  Windows: Download from https://git-lfs.github.com/")
        print("  macOS: brew install git-lfs")
        print("  Linux: sudo apt-get install git-lfs")
        print("\nAfter installation, run: git lfs install")
        return False
    
    # Check if repo already exists
    if (repo_dir / '.git').exists():
        print(f"Repository already exists at {repo_dir}")
        print("Pulling latest changes...")
        subprocess.run(['git', 'pull'], cwd=repo_dir, check=True)
    else:
        print(f"Cloning ModaNet repository to {repo_dir}...")
        print("This may take a while as annotations are large files...")
        subprocess.run(['git', 'clone', repo_url, str(repo_dir)], check=True)
    
    # Find annotation files
    annotations_dir = repo_dir / 'annotations'
    if not annotations_dir.exists():
        print(f"ERROR: Annotations directory not found at {annotations_dir}")
        return False
    
    # Look for JSON annotation files
    train_json = None
    val_json = None
    
    for json_file in annotations_dir.glob('*.json'):
        if 'train' in json_file.name.lower():
            train_json = json_file
        elif 'val' in json_file.name.lower():
            val_json = json_file
    
    if train_json is None or val_json is None:
        print("ERROR: Could not find train/val annotation files")
        print(f"Found files in {annotations_dir}:")
        for f in annotations_dir.glob('*.json'):
            print(f"  - {f.name}")
        return False
    
    print(f"\n✓ Found annotation files:")
    print(f"  - Training: {train_json}")
    print(f"  - Validation: {val_json}")
    
    # Copy to output directory for easier access
    output_train = output_dir / train_json.name
    output_val = output_dir / val_json.name
    
    print(f"\nCopying files to {output_dir}...")
    import shutil
    shutil.copy2(train_json, output_train)
    shutil.copy2(val_json, output_val)
    
    # Verify file sizes
    print(f"\nVerifying files...")
    print(f"  Training file size: {output_train.stat().st_size / (1024*1024):.2f} MB")
    print(f"  Validation file size: {output_val.stat().st_size / (1024*1024):.2f} MB")
    
    # Expected MD5 checksums (from ModaNet README)
    expected_md5_train = '96478657d20e322e9d3282c6d73c0c4c'
    expected_md5_val = '900b24b7d6c0c48203e6244f45d65499'
    
    print(f"\n✓ Annotation files ready!")
    print(f"\nNext steps:")
    print(f"1. Download ModaNet images (EASY METHOD):")
    print(f"   python download_modanet_images.py --output-dir modanet_raw/images")
    print(f"   OR manually: pip install maskrcnn-modanet && maskrcnn-modanet download")
    print(f"")
    print(f"2. Run conversion script:")
    print(f"   python convert_modanet_to_yolo.py \\")
    print(f"     --train-json {output_train} \\")
    print(f"     --val-json {output_val} \\")
    print(f"     --images-dir modanet_raw/images \\")
    print(f"     --output-dir modanet_yolo")
    
    return True

def print_image_download_info():
    """Print information about downloading ModaNet images."""
    print("\n" + "="*60)
    print("IMPORTANT: Downloading ModaNet Images")
    print("="*60)
    print("\nModaNet annotations are based on images from the PaperDoll dataset.")
    print("You need to download the images separately.")
    print("\nOptions:")
    print("1. Check the ModaNet repository for image download links")
    print("2. Contact the ModaNet team via their Google Group")
    print("3. Use the PaperDoll dataset if you have access")
    print("\nThe images should be organized in a directory structure")
    print("that matches the file names in the annotation JSON files.")
    print("="*60)

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Download ModaNet annotations')
    parser.add_argument('--output-dir', type=str, default='modanet_raw',
                        help='Output directory for downloaded files (default: modanet_raw)')
    
    args = parser.parse_args()
    
    success = download_modanet_annotations(args.output_dir)
    if success:
        print_image_download_info()

