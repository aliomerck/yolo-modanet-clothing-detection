# How to Download ModaNet Images

The `maskrcnn-modanet` package requires a Unix-like environment (bash). On Windows, you have several options:

## Option 1: Use Git Bash with Fixed Script (Recommended)

The `maskrcnn-modanet` tool has a path issue on Windows. Use this workaround:

1. **Open Git Bash** and navigate to your project:
   ```bash
   cd /path/to/yolo-modanet-clothing-detection
   ```

2. **Run the fixed download script**:
   ```bash
   bash fix_and_download.sh
   ```
   
   When prompted:
   - **Type `N`** and press Enter (for 50k ModaNet images, not 1 million)
   - This will download ~55,000 ModaNet images

**Alternative:** If the above doesn't work, try manually running the download script:
```bash
cd /c/Users/aliom/AppData/Roaming/Python/Python313/site-packages/maskrcnn_modanet
bash download.sh /path/to/yolo-modanet-clothing-detection/modanet_raw/images False
```

## Option 2: Use WSL (Windows Subsystem for Linux)

If you have WSL installed:

1. Open WSL terminal
2. Navigate to your project (you may need to access Windows files via `/mnt/c/...`)
3. Run: `maskrcnn-modanet datasets download [path]`

## Option 3: Manual Download (Alternative)

If the above methods don't work, you can:

1. **Contact ModaNet team**: https://groups.google.com/forum/#!forum/moda-net
2. **Check PaperDoll dataset**: ModaNet images are based on PaperDoll dataset
   - Repository: https://github.com/kyamagu/paperdoll
   - You may need to request access or find download links

## Option 4: Use Pre-processed Datasets

Some researchers have shared pre-processed ModaNet datasets. Check:
- Academic paper repositories
- Research dataset sharing platforms
- ModaNet GitHub issues/discussions

## After Downloading Images

Once you have the images in `modanet_raw/images/`, proceed with conversion:

```bash
python convert_modanet_to_yolo.py \
  --train-json modanet_raw/modanet2018_instances_train.json \
  --val-json modanet_raw/modanet2018_instances_val.json \
  --images-dir modanet_raw/images \
  --output-dir modanet_yolo
```

## Troubleshooting

**If you get "wget: command not found":**
- Install wget: See [INSTALL_TOOLS.md](INSTALL_TOOLS.md)
- Or run: `bash setup_gitbash_tools.sh` to try automatic installation
- Alternative: Use WSL which has all tools pre-installed

**If you get "tar: command not found":**
- tar should come with Git Bash
- If missing, reinstall Git for Windows
- Or use WSL

**If you get "bash not found" errors:**
- Use Git Bash instead of PowerShell
- Or install WSL

**If download is slow:**
- The 50k images are several GB in size
- The full PaperDoll dataset is 40GB
- Be patient, it may take hours depending on your connection

**If images don't match annotations:**
- Ensure image file names match those in the JSON annotation files
- Check that you downloaded the ModaNet subset (50k), not the full PaperDoll dataset

**Alternative if tools don't work:**
- Use WSL (Windows Subsystem for Linux) - has all tools pre-installed
- Or download the photos.lmdb.tar file manually if you have access

