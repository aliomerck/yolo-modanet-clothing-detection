"""
Run inference on images using trained YOLOv11 ModaNet model.
"""

from ultralytics import YOLO
from pathlib import Path
import argparse

def run_inference(
    model_path,
    source,
    conf=0.25,
    iou=0.45,
    imgsz=640,
    save=True,
    show=False,
    save_txt=False,
    save_conf=False
):
    """
    Run inference on images/videos using trained YOLOv11 model.
    
    Args:
        model_path: Path to trained model weights (.pt file)
        source: Image/video path or directory, or webcam (0)
        conf: Confidence threshold (default: 0.25)
        iou: IoU threshold for NMS (default: 0.45)
        imgsz: Image size for inference (default: 640)
        save: Whether to save results (default: True)
        show: Whether to display results (default: False)
        save_txt: Whether to save results as text files (default: False)
        save_conf: Whether to save confidence scores in text files (default: False)
    """
    # Load model
    print(f"Loading model from: {model_path}")
    model = YOLO(model_path)
    
    # Load class names
    try:
        # Try to get class names from model
        if hasattr(model, 'names'):
            class_names = model.names
            print(f"\nModel classes ({len(class_names)}):")
            for idx, name in class_names.items():
                print(f"  {idx}: {name}")
    except:
        print("Could not load class names from model")
    
    print(f"\nRunning inference on: {source}")
    print(f"Confidence threshold: {conf}")
    print(f"IoU threshold: {iou}")
    print(f"Image size: {imgsz}")
    
    # Run inference
    results = model.predict(
        source=source,
        conf=conf,
        iou=iou,
        imgsz=imgsz,
        save=save,
        show=show,
        save_txt=save_txt,
        save_conf=save_conf,
        line_width=2
    )
    
    # Print results summary
    print(f"\n{'='*50}")
    print("Inference Results:")
    print(f"{'='*50}")
    
    for i, result in enumerate(results):
        print(f"\nImage {i+1}: {result.path}")
        print(f"  Detections: {len(result.boxes)}")
        
        if len(result.boxes) > 0:
            print("  Detected items:")
            for box in result.boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                class_name = model.names[cls] if hasattr(model, 'names') else f"class_{cls}"
                bbox = box.xyxy[0].tolist()
                print(f"    - {class_name}: {conf:.2f} confidence, bbox: {bbox}")
    
    print(f"\n{'='*50}")
    if save:
        print(f"Results saved to: {results[0].save_dir}")
    
    return results

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run inference with trained YOLOv11 ModaNet model')
    parser.add_argument('--model', type=str, required=True,
                        help='Path to trained model weights (.pt file)')
    parser.add_argument('--source', type=str, required=True,
                        help='Image/video path, directory, or webcam (0)')
    parser.add_argument('--conf', type=float, default=0.25,
                        help='Confidence threshold (default: 0.25)')
    parser.add_argument('--iou', type=float, default=0.45,
                        help='IoU threshold for NMS (default: 0.45)')
    parser.add_argument('--imgsz', type=int, default=640,
                        help='Image size for inference (default: 640)')
    parser.add_argument('--no-save', action='store_true',
                        help='Do not save results')
    parser.add_argument('--show', action='store_true',
                        help='Display results')
    parser.add_argument('--save-txt', action='store_true',
                        help='Save results as text files')
    parser.add_argument('--save-conf', action='store_true',
                        help='Save confidence scores in text files')
    
    args = parser.parse_args()
    
    run_inference(
        model_path=args.model,
        source=args.source,
        conf=args.conf,
        iou=args.iou,
        imgsz=args.imgsz,
        save=not args.no_save,
        show=args.show,
        save_txt=args.save_txt,
        save_conf=args.save_conf
    )


