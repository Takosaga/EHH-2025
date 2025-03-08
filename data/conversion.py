import json
import os
import numpy as np
from pathlib import Path

def convert_coco_to_yolo(coco_json_path, output_dir, class_mapping=None):
    """
    Convert COCO format JSON annotations to YOLO format txt files.
    
    Args:
        coco_json_path (str): Path to the COCO JSON file
        output_dir (str): Directory to save the YOLO annotations
        class_mapping (dict, optional): Map from COCO category IDs to YOLO class indices
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Load COCO JSON data
    with open(coco_json_path, 'r') as f:
        coco_data = json.load(f)
    
    # Extract categories
    categories = coco_data['categories']
    if class_mapping is None:
        # Create class mapping (COCO category ID -> YOLO class index)
        class_mapping = {cat['id']: idx for idx, cat in enumerate(categories)}
    
    # Create a mapping from image_id to file_name
    image_id_to_filename = {img['id']: img['file_name'] for img in coco_data['images']}
    image_id_to_size = {img['id']: (img['width'], img['height']) for img in coco_data['images']}
    
    # Group annotations by image_id
    annotations_by_image = {}
    for ann in coco_data['annotations']:
        image_id = ann['image_id']
        if image_id not in annotations_by_image:
            annotations_by_image[image_id] = []
        annotations_by_image[image_id].append(ann)
    
    # Process each image
    for image_id, annotations in annotations_by_image.items():
        # Get image filename and size
        if image_id not in image_id_to_filename:
            print(f"Warning: Image ID {image_id} not found in images list. Skipping.")
            continue
            
        filename = image_id_to_filename[image_id]
        img_width, img_height = image_id_to_size[image_id]
        
        # Get base filename without extension
        base_filename = os.path.splitext(filename)[0]
        
        # Create YOLO annotation file
        yolo_filepath = os.path.join(output_dir, f"{base_filename}.txt")
        
        with open(yolo_filepath, 'w') as yolo_file:
            for ann in annotations:
                # Get category_id and map to YOLO class index
                category_id = ann['category_id']
                if category_id not in class_mapping:
                    print(f"Warning: Category ID {category_id} not in mapping. Skipping annotation.")
                    continue
                    
                yolo_class = class_mapping[category_id]
                
                # Handle ellipse by using the bounding box
                # YOLO format: <class_id> <x_center> <y_center> <width> <height>
                # where x, y, w, h are normalized by image dimensions
                
                x, y, w, h = ann['bbox']
                
                # Normalize coordinates
                x_center = (x + w/2) / img_width
                y_center = (y + h/2) / img_height
                norm_width = w / img_width
                norm_height = h / img_height
                
                # Write YOLO format line
                yolo_file.write(f"{yolo_class} {x_center:.6f} {y_center:.6f} {norm_width:.6f} {norm_height:.6f}\n")
    
    print(f"Conversion complete. YOLO annotations saved to {output_dir}")
    return class_mapping

def process_dataset_splits(dataset_dir):
    """
    Process all dataset splits (train, val, test) and create class mapping file.
    
    Args:
        dataset_dir (str): Root directory of the dataset
    """
    # Define paths
    json_dir = os.path.join(dataset_dir)
    train_json = os.path.join(json_dir, 'instances_Train.json')
    val_json = os.path.join(json_dir, 'instances_Validation.json')
    test_json = os.path.join(json_dir, 'instances_Test.json')
    
    # Create output directories
    labels_dir = os.path.join(dataset_dir, 'labels')
    train_dir = os.path.join(labels_dir, 'train')
    val_dir = os.path.join(labels_dir, 'val')
    test_dir = os.path.join(labels_dir, 'test')
    
    # Load the first available JSON to get categories
    json_paths = [p for p in [train_json, val_json, test_json] if os.path.exists(p)]
    if not json_paths:
        raise FileNotFoundError("No JSON annotation files found")
    
    with open(json_paths[0], 'r') as f:
        first_data = json.load(f)
    
    # Create class mapping
    categories = first_data['categories']
    class_mapping = {cat['id']: idx for idx, cat in enumerate(categories)}
    
    # Create names file (class names)
    with open(os.path.join(dataset_dir, 'data.yaml'), 'w') as f:
        f.write(f"# YOLOv11 dataset configuration\n")
        f.write(f"path: {os.path.abspath(dataset_dir)}\n")
        f.write(f"train: images/train\n")
        f.write(f"val: images/val\n")
        f.write(f"test: images/test\n\n")
        
        f.write(f"# Classes\n")
        f.write(f"names:\n")
        for cat in sorted(categories, key=lambda x: class_mapping[x['id']]):
            f.write(f"  {class_mapping[cat['id']]}: {cat['name']}\n")
    
    # Process each split
    if os.path.exists(train_json):
        convert_coco_to_yolo(train_json, train_dir, class_mapping)
    
    if os.path.exists(val_json):
        convert_coco_to_yolo(val_json, val_dir, class_mapping)
    
    if os.path.exists(test_json):
        convert_coco_to_yolo(test_json, test_dir, class_mapping)
    
    print(f"Dataset processing complete. Configuration saved to {os.path.join(dataset_dir, 'data.yaml')}")

if __name__ == "__main__":
    # Assume script is run from the dataset root directory
    dataset_dir = "."
    process_dataset_splits(dataset_dir)