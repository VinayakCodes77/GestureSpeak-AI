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
        return predicted_class, float(confidence)
