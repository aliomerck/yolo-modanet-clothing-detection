"""
Train YOLOv11 model on ModaNet dataset for clothing item detection.
"""

from ultralytics import YOLO
import torch
import os

def train_modanet_yolo(
    data_yaml='modanet_yolo/modanet.yaml',
    model_size='l',  # n, s, m, l, x
    epochs=100,
    imgsz=640,
    batch=16,
    device=None,
    project='runs/detect',
    name='modanet_yolov11',
    patience=50,
    save=True,
    plots=True
):
    """
    Train YOLOv11 model on ModaNet dataset.
    
    Args:
        data_yaml: Path to dataset YAML configuration file
        model_size: Model size - 'n' (nano), 's' (small), 'm' (medium), 'l' (large), 'x' (xlarge)
        epochs: Number of training epochs
        imgsz: Image size for training
        batch: Batch size
        device: Device to use (None for auto, 'cuda', 'cpu', or specific GPU ID)
        project: Project directory name
        name: Experiment name
        patience: Early stopping patience
        save: Whether to save checkpoints
        plots: Whether to generate training plots
    """
    # Auto-select device
    if device is None:
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    print(f"Using device: {device}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")
        print(f"CUDA version: {torch.version.cuda}")
    
    # Load YOLOv11 model
    model_name = f'yolo11{model_size}.pt'
    print(f"\nLoading model: {model_name}")
    model = YOLO(model_name)  # This will download pretrained weights if not available
    
    # Print model info
    print(f"\nModel: YOLOv11{model_size.upper()}")
    print(f"Dataset: {data_yaml}")
    print(f"Training parameters:")
    print(f"  - Epochs: {epochs}")
    print(f"  - Image size: {imgsz}")
    print(f"  - Batch size: {batch}")
    print(f"  - Device: {device}")
    print(f"  - Patience: {patience}")
    
    # Train the model
    print("\n" + "="*50)
    print("Starting training...")
    print("="*50 + "\n")
    
    results = model.train(
        data=data_yaml,
        epochs=epochs,
        imgsz=imgsz,
        batch=batch,
        device=device,
        project=project,
        name=name,
        patience=patience,
        save=save,
        plots=plots,
        # Additional training parameters for better performance
        optimizer='AdamW',
        lr0=0.01,  # Initial learning rate
        lrf=0.01,  # Final learning rate (lr0 * lrf)
        momentum=0.937,
        weight_decay=0.0005,
        warmup_epochs=3.0,
        warmup_momentum=0.8,
        warmup_bias_lr=0.1,
        box=7.5,  # Box loss gain
        cls=0.5,  # Class loss gain
        dfl=1.5,  # DFL loss gain
        pose=12.0,  # Pose loss gain (if applicable)
        kobj=1.0,  # Keypoint obj loss gain (if applicable)
        label_smoothing=0.0,
        nbs=64,  # Nominal batch size
        hsv_h=0.015,  # Image HSV-Hue augmentation
        hsv_s=0.7,  # Image HSV-Saturation augmentation
        hsv_v=0.4,  # Image HSV-Value augmentation
        degrees=0.0,  # Image rotation (+/- deg)
        translate=0.1,  # Image translation (+/- fraction)
        scale=0.5,  # Image scale (+/- gain)
        shear=0.0,  # Image shear (+/- deg)
        perspective=0.0,  # Image perspective (+/- fraction)
        flipud=0.0,  # Image flip up-down (probability)
        fliplr=0.5,  # Image flip left-right (probability)
        mosaic=1.0,  # Image mosaic (probability)
        mixup=0.0,  # Image mixup (probability)
        copy_paste=0.0,  # Segment copy-paste (probability)
    )
    
    print("\n" + "="*50)
    print("Training completed!")
    print("="*50)
    
    # Print results summary
    print(f"\nBest model saved to: {results.save_dir}/weights/best.pt")
    print(f"Last model saved to: {results.save_dir}/weights/last.pt")
    
    # Validate the model
    print("\nRunning validation...")
    metrics = model.val()
    print(f"\nValidation mAP50: {metrics.box.map50:.4f}")
    print(f"Validation mAP50-95: {metrics.box.map:.4f}")
    
    return model, results

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Train YOLOv11 on ModaNet dataset')
    parser.add_argument('--data', type=str, default='modanet_yolo/modanet.yaml',
                        help='Path to dataset YAML file (default: modanet_yolo/modanet.yaml)')
    parser.add_argument('--model', type=str, default='l', choices=['n', 's', 'm', 'l', 'x'],
                        help='Model size: n (nano), s (small), m (medium), l (large), x (xlarge) (default: l)')
    parser.add_argument('--epochs', type=int, default=100,
                        help='Number of training epochs (default: 100)')
    parser.add_argument('--imgsz', type=int, default=640,
                        help='Image size for training (default: 640)')
    parser.add_argument('--batch', type=int, default=16,
                        help='Batch size (default: 16)')
    parser.add_argument('--device', type=str, default=None,
                        help='Device to use: cuda, cpu, or GPU ID (default: auto)')
    parser.add_argument('--project', type=str, default='runs/detect',
                        help='Project directory (default: runs/detect)')
    parser.add_argument('--name', type=str, default='modanet_yolov11',
                        help='Experiment name (default: modanet_yolov11)')
    parser.add_argument('--patience', type=int, default=50,
                        help='Early stopping patience (default: 50)')
    
    args = parser.parse_args()
    
    train_modanet_yolo(
        data_yaml=args.data,
        model_size=args.model,
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        device=args.device,
        project=args.project,
        name=args.name,
        patience=args.patience
    )


