"""
Convert ModaNet COCO format annotations to YOLO format.
ModaNet dataset: https://github.com/eBay/modanet
"""

import json
import os
import shutil
from pathlib import Path
from tqdm import tqdm
import cv2

def convert_bbox_coco_to_yolo(bbox, img_width, img_height):
    """
    Convert COCO bbox format [x, y, width, height] to YOLO format [x_center, y_center, width, height] (normalized).
    
    Args:
        bbox: [x, y, width, height] in pixels
        img_width: Image width in pixels
        img_height: Image height in pixels
    
    Returns:
        [x_center, y_center, width, height] normalized to [0, 1]
    """
    x, y, w, h = bbox
    
    # Calculate center coordinates
    x_center = (x + w / 2) / img_width
    y_center = (y + h / 2) / img_height
    
    # Normalize width and height
    width = w / img_width
    height = h / img_height
    
    return [x_center, y_center, width, height]

def load_coco_annotations(json_path):
    """Load COCO format annotations from JSON file."""
    with open(json_path, 'r') as f:
        data = json.load(f)
    return data

def create_yolo_structure(output_dir):
    """Create YOLO dataset directory structure."""
    output_dir = Path(output_dir)
    (output_dir / 'images' / 'train').mkdir(parents=True, exist_ok=True)
    (output_dir / 'images' / 'val').mkdir(parents=True, exist_ok=True)
    (output_dir / 'labels' / 'train').mkdir(parents=True, exist_ok=True)
    (output_dir / 'labels' / 'val').mkdir(parents=True, exist_ok=True)
    return output_dir

def convert_modanet_to_yolo(
    train_json_path,
    val_json_path,
    images_dir,
    output_dir,
    class_mapping=None
):
    """
    Convert ModaNet dataset from COCO format to YOLO format.
    
    Args:
        train_json_path: Path to training annotations JSON
        val_json_path: Path to validation annotations JSON
        images_dir: Directory containing ModaNet images
        output_dir: Output directory for YOLO format dataset
        class_mapping: Optional dict to map category IDs to class indices
    """
    print("Loading COCO annotations...")
    train_data = load_coco_annotations(train_json_path)
    val_data = load_coco_annotations(val_json_path)
    
    # Create YOLO directory structure
    output_dir = create_yolo_structure(output_dir)
    
    # Build category mapping
    categories = {cat['id']: cat['name'] for cat in train_data['categories']}
    
    # Create class mapping (category_id -> class_index for YOLO)
    # YOLO uses 0-indexed classes, ModaNet uses 1-13
    if class_mapping is None:
        # Sort categories by ID to ensure consistent mapping
        sorted_cats = sorted(categories.items())
        class_mapping = {cat_id: idx for idx, (cat_id, _) in enumerate(sorted_cats)}
    
    # Save class names file (use same sorted order)
    sorted_cats = sorted(categories.items())
    class_names = [cat_name for _, cat_name in sorted_cats]
    with open(output_dir / 'classes.txt', 'w') as f:
        f.write('\n'.join(class_names))
    
    print(f"Found {len(class_names)} classes: {', '.join(class_names)}")
    
    # Process training set
    print("\nProcessing training set...")
    process_split(train_data, images_dir, output_dir, 'train', class_mapping)
    
    # Process validation set
    print("\nProcessing validation set...")
    process_split(val_data, images_dir, output_dir, 'val', class_mapping)
    
    # Create dataset YAML file for YOLO
    create_yolo_yaml(output_dir, class_names, len(class_names))
    
    print(f"\n✓ Conversion complete! Dataset saved to: {output_dir}")
    print(f"  - Training images: {len(train_data['images'])}")
    print(f"  - Validation images: {len(val_data['images'])}")
    print(f"  - Classes: {len(class_names)}")

def process_split(data, images_dir, output_dir, split_name, class_mapping):
    """Process a single split (train/val) of the dataset."""
    images_dir = Path(images_dir)
    output_dir = Path(output_dir)
    
    # Create image_id to image info mapping
    image_info = {img['id']: img for img in data['images']}
    
    # Group annotations by image_id
    annotations_by_image = {}
    for ann in data['annotations']:
        image_id = ann['image_id']
        if image_id not in annotations_by_image:
            annotations_by_image[image_id] = []
        annotations_by_image[image_id].append(ann)
    
    # Process each image
    for image_id, img_info in tqdm(image_info.items(), desc=f"Processing {split_name}"):
        file_name = img_info['file_name']
        img_width = img_info['width']
        img_height = img_info['height']
        
        # Source image path
        src_image_path = images_dir / file_name
        
        # Skip if image doesn't exist
        if not src_image_path.exists():
            print(f"Warning: Image not found: {src_image_path}")
            continue
        
        # Destination paths
        dst_image_path = output_dir / 'images' / split_name / file_name
        label_path = output_dir / 'labels' / split_name / (Path(file_name).stem + '.txt')
        
        # Copy image
        shutil.copy2(src_image_path, dst_image_path)
        
        # Create label file
        annotations = annotations_by_image.get(image_id, [])
        with open(label_path, 'w') as f:
            for ann in annotations:
                category_id = ann['category_id']
                class_idx = class_mapping[category_id]
                
                # Get bounding box
                bbox = ann['bbox']
                
                # Convert to YOLO format
                yolo_bbox = convert_bbox_coco_to_yolo(bbox, img_width, img_height)
                
                # Write to label file: class_id x_center y_center width height
                f.write(f"{class_idx} {' '.join(map(str, yolo_bbox))}\n")

def create_yolo_yaml(output_dir, class_names, num_classes):
    """Create YOLO dataset configuration YAML file."""
    yaml_content = f"""# ModaNet Dataset Configuration for YOLO
# Generated automatically from COCO format annotations

path: {Path(output_dir).absolute()}  # dataset root dir
train: images/train  # train images (relative to 'path')
val: images/val  # val images (relative to 'path')

# Classes
nc: {num_classes}  # number of classes
names: {class_names}  # class names
"""
    
    yaml_path = Path(output_dir) / 'modanet.yaml'
    with open(yaml_path, 'w') as f:
        f.write(yaml_content)
    
    print(f"\n✓ Created dataset config: {yaml_path}")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Convert ModaNet COCO format to YOLO format')
    parser.add_argument('--train-json', type=str, required=True,
                        help='Path to ModaNet training annotations JSON file')
    parser.add_argument('--val-json', type=str, required=True,
                        help='Path to ModaNet validation annotations JSON file')
    parser.add_argument('--images-dir', type=str, required=True,
                        help='Directory containing ModaNet images')
    parser.add_argument('--output-dir', type=str, default='modanet_yolo',
                        help='Output directory for YOLO format dataset (default: modanet_yolo)')
    
    args = parser.parse_args()
    
    convert_modanet_to_yolo(
        train_json_path=args.train_json,
        val_json_path=args.val_json,
        images_dir=args.images_dir,
        output_dir=args.output_dir
    )

