import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.neural_network import MLPClassifier
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, "dataset", "processed")
MODELS_DIR = os.path.join(BASE_DIR, "models")

def plot_confusion_matrix(y_true, y_pred, classes, save_path):
    """Plots confusion matrix."""
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(12, 10))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=classes, yticklabels=classes)
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.savefig(save_path)
    plt.close()

def train():
    if not os.path.exists(PROCESSED_DIR):
        print("Processed data not found. Please run preprocess_data.py first.")
        return
        
    print("Loading data...")
    X_train = np.load(os.path.join(PROCESSED_DIR, "X_train.npy"))
    y_train_raw = np.load(os.path.join(PROCESSED_DIR, "y_train.npy"), allow_pickle=True)
    X_val = np.load(os.path.join(PROCESSED_DIR, "X_val.npy"))
    y_val_raw = np.load(os.path.join(PROCESSED_DIR, "y_val.npy"), allow_pickle=True)
    X_test = np.load(os.path.join(PROCESSED_DIR, "X_test.npy"))
    y_test_raw = np.load(os.path.join(PROCESSED_DIR, "y_test.npy"), allow_pickle=True)
    
    # Encode labels
    encoder = LabelEncoder()
    y_train = encoder.fit_transform(y_train_raw)
    y_val = encoder.transform(y_val_raw)
    y_test = encoder.transform(y_test_raw)
    
    # Save encoded classes for inference
    os.makedirs(MODELS_DIR, exist_ok=True)
    np.save(os.path.join(MODELS_DIR, "classes.npy"), encoder.classes_)
    
    num_classes = len(encoder.classes_)
    
    print(f"Building MLP model for {num_classes} classes...")
    # Use Scikit-Learn MLPClassifier with very high capacity and extremely long training
    model = MLPClassifier(hidden_layer_sizes=(512, 256, 128), max_iter=5000, early_stopping=False, random_state=42, verbose=True)
    
    print("Starting training...")
    # Scikit-learn doesn't easily plot loss history in a Keras style without accessing loss_curve_, 
    # but we can combine train + val for sklearn's internal early stopping.
    X_combined = np.vstack((X_train, X_val))
    y_combined = np.hstack((y_train, y_val))
    
    model.fit(X_combined, y_combined)
    
    # Plot loss curve
    plt.figure()
    plt.plot(model.loss_curve_)
    plt.title('Training Loss')
    plt.xlabel('Iterations')
    plt.ylabel('Loss')
    plt.savefig(os.path.join(MODELS_DIR, "training_history.png"))
    plt.close()
    
    print("Evaluating on test set...")
    y_pred = model.predict(X_test)
    test_acc = accuracy_score(y_test, y_pred)
    print(f"Test Accuracy: {test_acc*100:.2f}%")
    
    print("Generating confusion matrix...")
    plot_confusion_matrix(y_test, y_pred, encoder.classes_, os.path.join(MODELS_DIR, "confusion_matrix.png"))
    
    model_save_path = os.path.join(MODELS_DIR, "gesturespeak_model.pkl")
    joblib.dump(model, model_save_path)
    
    print("Training complete. Model and artifacts saved in models/ directory.")

if __name__ == "__main__":
    train()
