# Installing Required Tools for ModaNet Download

The ModaNet download script requires `wget` and `tar` which aren't included in Git Bash by default.

## Option 1: Install wget and tar in Git Bash (Recommended)

If you have MSYS2/MinGW-w64 installed with Git Bash, you can install these tools:

```bash
# In Git Bash, try:
pacman -S wget tar
```

If `pacman` is not available, you can:

1. **Download wget for Windows:**
   - Download from: https://eternallybored.org/misc/wget/
   - Extract `wget.exe` to a directory in your PATH (e.g., `C:\Program Files\Git\usr\bin\`)
   - Or add the directory to your PATH

2. **tar is usually included with Git Bash**, but if not:
   - It should be in `C:\Program Files\Git\usr\bin\tar.exe`
   - If missing, reinstall Git for Windows

## Option 2: Use WSL (Windows Subsystem for Linux)

WSL has all the required tools pre-installed:

```bash
# In WSL terminal:
sudo apt-get update
sudo apt-get install wget tar git-lfs
```

Then run the download script from WSL.

## Option 3: Download the LMDB File Manually

If you have the 40GB `photos.lmdb.tar` file:

1. Place it in: `modanet_raw/datasets/paperdoll/data/chictopia/`
2. Extract it: `tar -xf photos.lmdb.tar`
3. The script will detect it and skip the download

## Option 4: Use Python Alternative (Limited)

I've created `download_modanet_simple.py` which tries to download images directly,
but this may not work if images require authentication or aren't publicly accessible.

```bash
python download_modanet_simple.py --train-json modanet_raw/modanet2018_instances_train.json --val-json modanet_raw/modanet2018_instances_val.json
```

## Quick Check

To check if tools are available:

```bash
# In Git Bash:
which wget
which tar

# If both show paths, you're good to go!
```


