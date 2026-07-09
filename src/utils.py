import os
import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

def init_mediapipe_hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5):
    """Initializes and returns the MediaPipe Hands object."""
    return mp_hands.Hands(
        static_image_mode=static_image_mode,
        max_num_hands=max_num_hands,
        min_detection_confidence=min_detection_confidence,
        min_tracking_confidence=min_tracking_confidence
    )

def extract_landmarks(hand_landmarks):
    """
    Extracts x, y, z coordinates from MediaPipe hand landmarks
    and normalizes them relative to the wrist (landmark 0).
    """
    landmarks = []
    # Wrist is the 0th landmark
    base_x = hand_landmarks.landmark[0].x
    base_y = hand_landmarks.landmark[0].y
    base_z = hand_landmarks.landmark[0].z

    for lm in hand_landmarks.landmark:
        landmarks.append(lm.x - base_x)
        landmarks.append(lm.y - base_y)
        landmarks.append(lm.z - base_z)
        
    # Flatten the list of lists into a 1D array of length 63 (21 landmarks * 3 coordinates)
    return np.array(landmarks)

def draw_landmarks(image, hand_landmarks):
    """Draws hand landmarks on the image."""
    mp_drawing.draw_landmarks(
        image,
        hand_landmarks,
        mp_hands.HAND_CONNECTIONS,
        mp_drawing_styles.get_default_hand_landmarks_style(),
        mp_drawing_styles.get_default_hand_connections_style()
    )

def ensure_dir(directory):
    """Ensures a directory exists."""
    if not os.path.exists(directory):
        os.makedirs(directory)
