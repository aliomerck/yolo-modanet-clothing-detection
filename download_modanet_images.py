"""
Download ModaNet images using the maskrcnn-modanet package.
This is the easiest way to get all ModaNet images.
"""

import subprocess
import sys
from pathlib import Path

def install_maskrcnn_modanet():
    """Install the maskrcnn-modanet package if not already installed."""
    try:
        import maskrcnn_modanet
        print("✓ maskrcnn-modanet is already installed")
        return True
    except ImportError:
        print("Installing maskrcnn-modanet package...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "maskrcnn-modanet"])
            print("✓ maskrcnn-modanet installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("✗ Failed to install maskrcnn-modanet")
            return False

def download_modanet_images(output_dir='modanet_raw/images'):
    """
    Download ModaNet images using maskrcnn-modanet package.
    
    Args:
        output_dir: Directory to save images (default: modanet_raw/images)
    """
    # Install package if needed
    if not install_maskrcnn_modanet():
        print("\nERROR: Could not install maskrcnn-modanet package")
        print("Please try manually: pip install maskrcnn-modanet")
        return False
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Create config directory for maskrcnn-modanet
    config_dir = Path.home() / '.maskrcnn-modanet'
    config_dir.mkdir(exist_ok=True)
    
    print(f"\nDownloading ModaNet images to: {output_path.absolute()}")
    print("This may take a while (~55,000 images)...")
    print("="*60)
    
    # Try multiple methods to use maskrcnn-modanet
    success = False
    
    # Method 1: Try using the command-line tool directly
    script_path = Path.home() / 'AppData' / 'Roaming' / 'Python' / 'Python313' / 'Scripts' / 'maskrcnn-modanet.exe'
    if script_path.exists():
        try:
            print(f"Using command-line tool: {script_path}")
            print(f"Command: maskrcnn-modanet datasets download {output_path}")
            print("\nNOTE: The tool will ask if you want 1 million images (Y) or 50k ModaNet images (N).")
            print("We recommend choosing N for 50k ModaNet images.")
            print("\nStarting download (this may take a while)...")
            
            # Run with input 'N' for 50k images
            result = subprocess.run(
                [str(script_path), 'datasets', 'download', str(output_path)],
                input='N\n',
                text=True,
                check=True
            )
            success = True
        except subprocess.CalledProcessError as e:
            print(f"\nCommand failed with exit code {e.returncode}")
            if e.stdout:
                print(f"Output: {e.stdout}")
            if e.stderr:
                print(f"Error: {e.stderr}")
            print("\nNOTE: The maskrcnn-modanet tool may require bash/Unix environment.")
            print("You may need to run this manually or use WSL/Git Bash on Windows.")
    
    # Method 2: Try using CLI module
    if not success:
        try:
            from maskrcnn_modanet.cli import main
            import sys
            # Save original argv
            original_argv = sys.argv.copy()
            # Set up command-line arguments for download
            sys.argv = ['maskrcnn-modanet', 'download', '--output', str(output_path)]
            try:
                main()
                success = True
            finally:
                # Restore original argv
                sys.argv = original_argv
        except Exception as e:
            print(f"CLI module method failed: {e}")
            # Try direct function call if available
            try:
                from maskrcnn_modanet import download
                download(output_dir=str(output_path))
                success = True
            except:
                pass
    
    # Method 3: Try subprocess with python -m
    if not success:
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'maskrcnn_modanet', 'download'],
                check=True,
                cwd=str(output_path.parent)
            )
            success = True
        except:
            pass
    
    if success:
        print("\n" + "="*60)
        print("✓ Download complete!")
        print(f"Images saved to: {output_path.absolute()}")
        
        # Count downloaded images
        image_files = list(output_path.glob('*.jpg')) + list(output_path.glob('*.png'))
        print(f"Total images downloaded: {len(image_files)}")
        return True
    else:
        print("\n" + "="*60)
        print("✗ Automated download failed")
        print("="*60)
        print("\nThe maskrcnn-modanet tool requires bash/Unix environment.")
        print("\nSOLUTION: Use Git Bash (recommended for Windows):")
        print("1. Open Git Bash (comes with Git for Windows)")
        print("2. Navigate to your project directory")
        print(f"3. Run: maskrcnn-modanet datasets download {output_path}")
        print("4. When prompted, type 'N' for 50k ModaNet images")
        print("\nFor detailed instructions, see: DOWNLOAD_IMAGES.md")
        print("\nAlternative: Contact ModaNet team: https://groups.google.com/forum/#!forum/moda-net")
        return False

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Download ModaNet images')
    parser.add_argument('--output-dir', type=str, default='modanet_raw/images',
                        help='Output directory for images (default: modanet_raw/images)')
    
    args = parser.parse_args()
    
    success = download_modanet_images(args.output_dir)
    if success:
        print("\nNext step: Convert to YOLO format")
        print("python convert_modanet_to_yolo.py \\")
        print("  --train-json modanet_raw/modanet2018_instances_train.json \\")
        print("  --val-json modanet_raw/modanet2018_instances_val.json \\")
        print("  --images-dir modanet_raw/images \\")
        print("  --output-dir modanet_yolo")
    else:
        sys.exit(1)

