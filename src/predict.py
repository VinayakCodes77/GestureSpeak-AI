import os
import numpy as np
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODELS_DIR, "gesturespeak_model.pkl")
CLASSES_PATH = os.path.join(MODELS_DIR, "classes.npy")

class GesturePredictor:
    def __init__(self):
        self.model = None
        self.classes = None
        self.load_model()
        
    def load_model(self):
        if os.path.exists(MODEL_PATH) and os.path.exists(CLASSES_PATH):
            try:
                self.model = joblib.load(MODEL_PATH)
                self.classes = np.load(CLASSES_PATH, allow_pickle=True)
                print("Model loaded successfully.")
            except Exception as e:
                print(f"Error loading model: {e}")
        else:
            print("Model not found. Please train the model first. Using dummy prediction mode.")
            
    def predict(self, landmarks):
        """Predicts the gesture class given hand landmarks."""
        if self.model is None or self.classes is None:
            # Fallback/Dummy logic if model not loaded
            return "N/A", 0.0
            
        # Reshape landmarks for model input (1, num_features)
        input_data = np.expand_dims(landmarks, axis=0)
        
        # Predict class probabilities
        probabilities = self.model.predict_proba(input_data)[0]
        
        # Get class index and confidence
        class_index = np.argmax(probabilities)
        confidence = probabilities[class_index]
        
        predicted_class = self.classes[class_index]
        
        # --- HEURISTIC FIX FOR D vs O CONFUSION ---
        # The model sometimes confuses D and O because they look similar.
        # But physically, in a 'D', the index finger is extended straight UP.
        # In an 'O', the index finger is curled DOWN to touch the thumb.
        # We can check the Y coordinate of the Index Finger Tip (Landmark 8 -> index 25)
        # compared to the Index Finger PIP joint (Landmark 6 -> index 19).
        # Since Y decreases as it goes UP the screen:
        # If tip Y is significantly LESS than PIP Y, the finger is extended -> 'D'.
        if predicted_class in ['D', 'O']:
            index_tip_y = landmarks[25]
            index_pip_y = landmarks[19]
            
            # If the tip is above the PIP joint (extended upwards)
            if index_tip_y < index_pip_y - 0.05:
                predicted_class = 'D'
            else:
                predicted_class = 'O'
                
        return predicted_class, float(confidence)
