import os
import cv2
import mediapipe as mp
import pandas as pd
from src.utils import init_mediapipe_hands, extract_landmarks

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_DATASET_DIR = os.path.join(BASE_DIR, "dataset", "asl_alphabet_train", "asl_alphabet_train")
OUTPUT_DIR = os.path.join(BASE_DIR, "dataset", "train")

# Map kaggle folder names to our model classes
CLASS_MAP = {
    "del": "Delete",
    "space": "Space",
    "nothing": "Clear"
}

def extract_from_images(max_images_per_class=200):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    hands = init_mediapipe_hands(static_image_mode=True)
    
    if not os.path.exists(IMAGE_DATASET_DIR):
        print(f"Error: Could not find image dataset at {IMAGE_DATASET_DIR}")
        return

    print("Starting MediaPipe extraction on real Kaggle images...")
    
    for folder_name in os.listdir(IMAGE_DATASET_DIR):
        folder_path = os.path.join(IMAGE_DATASET_DIR, folder_name)
        if not os.path.isdir(folder_path):
            continue
            
        # Determine the target class name
        target_class = CLASS_MAP.get(folder_name.lower(), folder_name.upper())
        
        # Prepare CSV output
        output_csv = os.path.join(OUTPUT_DIR, f"{target_class}_raw.csv")
        
        # If we already have the synthetic file, we should overwrite it. We'll build a list of rows.
        rows = []
        
        image_files = os.listdir(folder_path)
        print(f"Processing class '{target_class}' (Found {len(image_files)} images, extracting up to {max_images_per_class})...")
        
        extracted_count = 0
        for img_name in image_files:
            if extracted_count >= max_images_per_class:
                break
                
            img_path = os.path.join(folder_path, img_name)
            image = cv2.imread(img_path)
            
            if image is None:
                continue
                
            # Convert to RGB for MediaPipe
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image_rgb)
            
            # If MediaPipe detects a hand, extract its landmarks
            if results.multi_hand_landmarks:
                # We only take the first hand found in the image
                hand_landmarks = results.multi_hand_landmarks[0]
                landmarks = extract_landmarks(hand_landmarks)
                
                # Append to our dataset format: [x0, y0, z0, ... x20, y20, z20, label]
                row = list(landmarks) + [target_class]
                rows.append(row)
                extracted_count += 1
                
        if len(rows) > 0:
            # Generate column names (0 to 62, then 'label')
            columns = [str(i) for i in range(len(rows[0]) - 1)] + ["label"]
            df = pd.DataFrame(rows, columns=columns)
            df.to_csv(output_csv, index=False)
            print(f"Successfully saved {len(rows)} real landmark sets for '{target_class}' to {output_csv}")
        else:
            print(f"Warning: MediaPipe could not detect any hands in the images for '{target_class}'.")

if __name__ == "__main__":
    extract_from_images(max_images_per_class=500)
