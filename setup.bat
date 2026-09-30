@echo off
REM Quick setup script for YOLOv11 ModaNet project (Windows)

echo ==========================================
echo YOLOv11 ModaNet Setup Script
echo ==========================================
echo.

REM Check Python version
echo Checking Python version...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    exit /b 1
)

REM Check if Git LFS is installed
echo.
echo Checking Git LFS installation...
git lfs version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git LFS is not installed
    echo Please install Git LFS from: https://git-lfs.github.com/
    exit /b 1
) else (
    echo Git LFS is installed
    git lfs install
)

REM Install Python dependencies
echo.
echo Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    exit /b 1
)

echo.
echo ==========================================
echo Setup complete!
echo ==========================================
echo.
echo Next steps:
echo 1. Download ModaNet annotations:
echo    python download_modanet.py
echo.
echo 2. Download ModaNet images (see README.md for instructions)
echo.
echo 3. Convert to YOLO format:
echo    python convert_modanet_to_yolo.py --train-json modanet_raw/modanet2018_instances_train.json --val-json modanet_raw/modanet2018_instances_val.json --images-dir modanet_raw/images --output-dir modanet_yolo
echo.
echo 4. Train the model:
echo    python train_yolo.py --data modanet_yolo/modanet.yaml --model l
echo.

pause


