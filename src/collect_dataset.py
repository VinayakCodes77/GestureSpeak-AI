import os
import cv2
import numpy as np
import pandas as pd
from utils import init_mediapipe_hands, extract_landmarks, draw_landmarks, ensure_dir

# Configuration
# Adjust paths if running from the root instead of src/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
TRAIN_DIR = os.path.join(DATASET_DIR, "train")
VALIDATION_DIR = os.path.join(DATASET_DIR, "validation")
TEST_DIR = os.path.join(DATASET_DIR, "test")

# Define ASL Alphabet + Space + Delete + Clear
CLASSES = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + ["Space", "Delete", "Clear"]
FRAMES_PER_CLASS = 200  # Reduced for faster data collection, can be increased to 500-1000

def main():
    # Ensure directories exist
    ensure_dir(TRAIN_DIR)
    ensure_dir(VALIDATION_DIR)
    ensure_dir(TEST_DIR)

    hands = init_mediapipe_hands()
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print("--- GestureSpeak AI Dataset Collection ---")
    print("Press 'q' to quit at any time.")
    print("Press 'c' to start collecting for the current class.")
    print("Press 'n' to skip to the next class.")

    for class_name in CLASSES:
        print(f"\nPrepare to collect data for class: '{class_name}'")
        
        # Wait for user to be ready
        while True:
            success, image = cap.read()
            if not success:
                break
            
            image = cv2.flip(image, 1)
            cv2.putText(image, f"Class: {class_name}. Press 'c' to start.", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.imshow('Data Collection', image)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('c'):
                break
            elif key == ord('n'):
                print(f"Skipping class: '{class_name}'")
                break
            elif key == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return

        if key == ord('n'):
            continue

        print(f"Collecting data for '{class_name}'...")
        collected_data = []
        frames_collected = 0

        while frames_collected < FRAMES_PER_CLASS:
            success, image = cap.read()
            if not success:
                break

            image = cv2.flip(image, 1)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image_rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    draw_landmarks(image, hand_landmarks)
                    landmarks = extract_landmarks(hand_landmarks)
                    collected_data.append(landmarks)
                    frames_collected += 1
                    break # collect one hand max per frame

            # Progress feedback
            cv2.putText(image, f"Collecting: {class_name}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(image, f"Frames: {frames_collected}/{FRAMES_PER_CLASS}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            cv2.imshow('Data Collection', image)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return

        if collected_data:
            # Save data to CSV
            df = pd.DataFrame(collected_data)
            df['label'] = class_name
            # For simplicity, save raw data in the train directory.
            # train_model.py will handle merging and splitting.
            csv_path = os.path.join(TRAIN_DIR, f"{class_name}_raw.csv")
            df.to_csv(csv_path, index=False)
            print(f"Saved {frames_collected} frames to {csv_path}")

    cap.release()
    cv2.destroyAllWindows()
    print("Data collection complete.")

if __name__ == "__main__":
    main()
