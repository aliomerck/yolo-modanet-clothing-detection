# YOLOv11 ModaNet Clothing Detection

This project trains YOLOv11 on the ModaNet dataset to detect and localize clothing items with precise bounding boxes.

## Dataset

**ModaNet** is a large-scale street fashion dataset with polygon annotations. It contains 13 clothing categories:
1. bag
2. belt
3. boots
4. footwear
5. outer (coat/jacket/suit/blazers/cardigan/sweater/jumpsuits/rompers/vest)
6. dress (dress/t-shirt dress)
7. sunglasses
8. pants (pants/jeans/leggings)
9. top (top/blouse/t-shirt/shirt)
10. shorts
11. skirt
12. headwear
13. scarf & tie

**Dataset Source**: [ModaNet GitHub Repository](https://github.com/eBay/modanet)

## Requirements

- Python 3.8+
- CUDA-capable GPU (recommended for training)
- Git LFS (for downloading annotations)

## Installation

1. **Install Git LFS** (required for downloading annotation files):
   - Windows: Download from [git-lfs.github.com](https://git-lfs.github.com/)
   - macOS: `brew install git-lfs`
   - Linux: `sudo apt-get install git-lfs`
   - After installation: `git lfs install`

2. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

## Setup Dataset

### Step 1: Download ModaNet Annotations

```bash
python download_modanet.py --output-dir modanet_raw
```

This will:
- Clone the ModaNet repository
- Extract annotation JSON files
- Save them to `modanet_raw/` directory

### Step 2: Download ModaNet Images

**Important:** The `maskrcnn-modanet` tool requires a Unix-like environment (bash). On Windows, use **Git Bash**.

**Method 1: Using Git Bash (Recommended for Windows):**

1. Open **Git Bash** (comes with Git for Windows)
2. Navigate to your project:
   ```bash
   cd /path/to/yolo-modanet-clothing-detection
   ```
3. Run the download command:
   ```bash
   maskrcnn-modanet datasets download modanet_raw/images
   ```
4. When prompted, type **`N`** and press Enter (for 50k ModaNet images)

**Method 2: Python Script (may require bash):**

```bash
pip install maskrcnn-modanet
python download_modanet_images.py --output-dir modanet_raw/images
```

**Note:** If you get bash errors, use Method 1 (Git Bash) instead.

**For detailed instructions and troubleshooting, see:** [DOWNLOAD_IMAGES.md](DOWNLOAD_IMAGES.md)

### Step 3: Convert to YOLO Format

Once you have both annotations and images:

```bash
python convert_modanet_to_yolo.py \
    --train-json modanet_raw/modanet2018_instances_train.json \
    --val-json modanet_raw/modanet2018_instances_val.json \
    --images-dir modanet_raw/images \
    --output-dir modanet_yolo
```

This will:
- Convert COCO format annotations to YOLO format
- Organize images and labels in YOLO directory structure
- Create `modanet.yaml` configuration file

## Training

### Basic Training

```bash
python train_yolo.py \
    --data modanet_yolo/modanet.yaml \
    --model l \
    --epochs 100 \
    --batch 16 \
    --imgsz 640
```

### Training Options

- `--model`: Model size - `n` (nano), `s` (small), `m` (medium), `l` (large), `x` (xlarge)
  - **Recommended**: `l` (large) for best accuracy/speed balance
  - Use `n` or `s` for faster training/inference, `x` for maximum accuracy
- `--epochs`: Number of training epochs (default: 100)
- `--batch`: Batch size (adjust based on GPU memory)
- `--imgsz`: Image size (default: 640, can use 1280 for higher accuracy)
- `--device`: Device (`cuda`, `cpu`, or GPU ID)
- `--patience`: Early stopping patience (default: 50)

### Example: Training with Different Model Sizes

**Fast training (nano model)**:
```bash
python train_yolo.py --model n --epochs 50 --batch 32
```

**High accuracy (xlarge model)**:
```bash
python train_yolo.py --model x --epochs 150 --batch 8 --imgsz 1280
```

## Model Selection Guide

Based on your use case, here are recommendations:

| Model | Speed | Accuracy | Use Case |
|-------|-------|----------|----------|
| **YOLOv11n** | Fastest | Good | Real-time inference, mobile deployment |
| **YOLOv11s** | Fast | Better | Balanced speed/accuracy |
| **YOLOv11m** | Medium | Good | General purpose |
| **YOLOv11l** | Slower | Better | **Recommended for clothing detection** |
| **YOLOv11x** | Slowest | Best | Maximum accuracy, offline processing |

**For precise clothing item detection, we recommend YOLOv11l** as it provides the best balance between accuracy and inference speed.

## Results

After training, results will be saved in `runs/detect/modanet_yolov11/`:
- `weights/best.pt` - Best model checkpoint
- `weights/last.pt` - Last epoch checkpoint
- Training plots and metrics
- Validation results

## Inference

Use the trained model for inference:

```python
from ultralytics import YOLO

# Load trained model
model = YOLO('runs/detect/modanet_yolov11/weights/best.pt')

# Run inference
results = model('path/to/image.jpg')

# Display results
results[0].show()

# Get bounding boxes
for result in results:
    boxes = result.boxes
    for box in boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])
        bbox = box.xyxy[0].tolist()
        print(f"Class: {cls}, Confidence: {conf:.2f}, BBox: {bbox}")
```

## Project Structure

```
yolo-modanet-clothing-detection/
├── requirements.txt              # Python dependencies
├── download_modanet.py           # Download ModaNet annotations
├── convert_modanet_to_yolo.py   # Convert COCO to YOLO format
├── train_yolo.py                 # Training script
├── README.md                     # This file
├── modanet_raw/                  # Raw dataset (after download)
│   ├── modanet2018_instances_train.json
│   ├── modanet2018_instances_val.json
│   └── images/                   # ModaNet images
├── modanet_yolo/                 # YOLO format dataset (after conversion)
│   ├── images/
│   │   ├── train/
│   │   └── val/
│   ├── labels/
│   │   ├── train/
│   │   └── val/
│   ├── classes.txt
│   └── modanet.yaml
└── runs/                         # Training results
    └── detect/
        └── modanet_yolov11/
```

## Troubleshooting

### Git LFS Issues
If annotation files are empty or corrupted:
```bash
cd modanet_raw/modanet_repo
git lfs pull
```

### CUDA Out of Memory
Reduce batch size:
```bash
python train_yolo.py --batch 8  # or 4, 2
```

### Missing Images
Ensure image file names in your images directory match those in the annotation JSON files.

## Citation

If you use ModaNet in your research, please cite:

```bibtex
@inproceedings{zheng/2018acmmm,
  author       = {Shuai Zheng and Fan Yang and M. Hadi Kiapour and Robinson Piramuthu},
  title        = {ModaNet: A Large-Scale Street Fashion Dataset with Polygon Annotations},
  booktitle    = {ACM Multimedia},
  year         = {2018},
}
```

## License

ModaNet annotations are released under Creative Commons Attribution-NonCommercial 4.0 license.

