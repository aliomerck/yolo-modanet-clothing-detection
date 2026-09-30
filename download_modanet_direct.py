"""
Direct download script for ModaNet images.
This script downloads images directly from the PaperDoll/Chictopia source
that ModaNet is based on, matching them with ModaNet annotations.
"""

import json
import requests
from pathlib import Path
from tqdm import tqdm
import time
import os

def load_modanet_annotations(train_json_path, val_json_path):
    """Load ModaNet annotation files to get image file names."""
    print("Loading ModaNet annotations...")
    
    with open(train_json_path, 'r') as f:
        train_data = json.load(f)
    with open(val_json_path, 'r') as f:
        val_data = json.load(f)
    
    # Get all image file names
    train_images = {img['file_name']: img for img in train_data['images']}
    val_images = {img['file_name']: img for img in val_data['images']}
    
    all_images = {**train_images, **val_images}
    print(f"Found {len(all_images)} unique images in annotations")
    
    return all_images

def download_image_from_chictopia(file_name, output_dir, base_url=None):
    """
    Download an image from Chictopia/PaperDoll.
    
    Note: This is a placeholder. The actual download URLs need to be
    determined from the PaperDoll dataset structure.
    """
    # PaperDoll images are typically organized by user/post ID
    # The file_name in ModaNet annotations should match the source
    
    output_path = Path(output_dir) / file_name
    
    # Skip if already downloaded
    if output_path.exists():
        return True
    
    # Try different possible URL patterns
    # This is a simplified approach - actual URLs may vary
    possible_urls = [
        f"https://s3.amazonaws.com/chictopia/images/{file_name}",
        f"https://chictopia.com/images/{file_name}",
        # Add more patterns based on actual PaperDoll structure
    ]
    
    for url in possible_urls:
        try:
            response = requests.get(url, timeout=10, stream=True)
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                return True
        except:
            continue
    
    return False

def download_modanet_images_direct(
    train_json_path,
    val_json_path,
    output_dir='modanet_raw/images',
    max_images=None
):
    """
    Download ModaNet images directly.
    
    WARNING: This is a workaround. The actual PaperDoll dataset
    may require authentication or have different URL structures.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Load annotations
    images = load_modanet_annotations(train_json_path, val_json_path)
    
    if max_images:
        images = dict(list(images.items())[:max_images])
    
    print(f"\nAttempting to download {len(images)} images...")
    print("="*60)
    print("\nNOTE: Direct download from Chictopia may not work due to:")
    print("1. URL structure changes")
    print("2. Authentication requirements")
    print("3. Rate limiting")
    print("\nRecommended: Use maskrcnn-modanet tool in Git Bash/WSL")
    print("="*60)
    
    downloaded = 0
    failed = 0
    
    for file_name, img_info in tqdm(images.items(), desc="Downloading"):
        if download_image_from_chictopia(file_name, output_path):
            downloaded += 1
        else:
            failed += 1
            # Rate limiting - wait a bit
            time.sleep(0.1)
    
    print(f"\n{'='*60}")
    print(f"Download complete!")
    print(f"  Successfully downloaded: {downloaded}")
    print(f"  Failed: {failed}")
    print(f"  Total: {len(images)}")
    
    if failed > 0:
        print(f"\n⚠ {failed} images could not be downloaded automatically.")
        print("You may need to:")
        print("1. Use the maskrcnn-modanet tool in Git Bash/WSL")
        print("2. Contact ModaNet team for direct download links")
        print("3. Access PaperDoll dataset directly if you have credentials")
    
    return downloaded > 0

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Direct download of ModaNet images (workaround method)'
    )
    parser.add_argument('--train-json', type=str,
                        default='modanet_raw/modanet2018_instances_train.json',
                        help='Path to training annotations')
    parser.add_argument('--val-json', type=str,
                        default='modanet_raw/modanet2018_instances_val.json',
                        help='Path to validation annotations')
    parser.add_argument('--output-dir', type=str, default='modanet_raw/images',
                        help='Output directory for images')
    parser.add_argument('--max-images', type=int, default=None,
                        help='Maximum number of images to download (for testing)')
    
    args = parser.parse_args()
    
    # Check if annotation files exist
    if not Path(args.train_json).exists() or not Path(args.val_json).exists():
        print("ERROR: Annotation files not found!")
        print(f"  Train JSON: {args.train_json}")
        print(f"  Val JSON: {args.val_json}")
        print("\nPlease download annotations first:")
        print("  python download_modanet.py")
        exit(1)
    
    download_modanet_images_direct(
        args.train_json,
        args.val_json,
        args.output_dir,
        args.max_images
    )


