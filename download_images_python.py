"""
Alternative method to download ModaNet images using Python directly.
This works around the PATH issue in Git Bash.
"""

import subprocess
import sys
from pathlib import Path

def find_maskrcnn_modanet():
    """Find the maskrcnn-modanet executable."""
    # Common locations
    possible_paths = [
        Path.home() / 'AppData' / 'Roaming' / 'Python' / 'Python313' / 'Scripts' / 'maskrcnn-modanet.exe',
        Path.home() / 'AppData' / 'Local' / 'Programs' / 'Python' / 'Python313' / 'Scripts' / 'maskrcnn-modanet.exe',
        Path('C:/Python313/Scripts/maskrcnn-modanet.exe'),
    ]
    
    for path in possible_paths:
        if path.exists():
            return path
    
    return None

def download_images(output_dir='modanet_raw/images'):
    """Download ModaNet images."""
    exe_path = find_maskrcnn_modanet()
    
    if not exe_path:
        print("ERROR: Could not find maskrcnn-modanet.exe")
        print("\nPlease ensure maskrcnn-modanet is installed:")
        print("  pip install maskrcnn-modanet")
        print("\nOr use Git Bash with the download_images_gitbash.sh script")
        return False
    
    print(f"Found maskrcnn-modanet at: {exe_path}")
    print(f"\nDownloading images to: {output_dir}")
    print("When prompted, type 'N' for 50k ModaNet images (recommended)")
    print("="*60)
    
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    try:
        # Run the command
        result = subprocess.run(
            [str(exe_path), 'datasets', 'download', output_dir],
            text=True,
            input='N\n'  # Automatically answer 'N' for 50k images
        )
        
        if result.returncode == 0:
            print("\n" + "="*60)
            print("✓ Download complete!")
            return True
        else:
            print(f"\nDownload failed with exit code: {result.returncode}")
            return False
            
    except Exception as e:
        print(f"\nError: {e}")
        print("\nTry running manually in Git Bash:")
        print(f"  {exe_path} datasets download {output_dir}")
        return False

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Download ModaNet images')
    parser.add_argument('--output-dir', type=str, default='modanet_raw/images',
                        help='Output directory for images')
    
    args = parser.parse_args()
    
    success = download_images(args.output_dir)
    sys.exit(0 if success else 1)


