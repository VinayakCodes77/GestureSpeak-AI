import os
import glob
import pandas as pd
from sklearn.model_selection import train_test_split

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
TRAIN_DIR = os.path.join(DATASET_DIR, "train")

def load_and_preprocess_data():
    """Loads raw CSVs, combines them, and splits into train, val, and test sets."""
    csv_files = glob.glob(os.path.join(TRAIN_DIR, "*_raw.csv"))
    
    if not csv_files:
        print("No raw dataset found. Please run collect_dataset.py first.")
        return False
        
    df_list = []
    for file in csv_files:
        df = pd.read_csv(file)
        df_list.append(df)
        
    combined_df = pd.concat(df_list, ignore_index=True)
    print(f"Total samples combined: {len(combined_df)}")
    
    # Split features and labels
    # Split features and labels - explicit to_numpy to avoid PyArrow split issues
    X = combined_df.iloc[:, :-1].to_numpy(dtype=float)
    y = combined_df.iloc[:, -1].to_numpy(dtype=str)
    
    print(f"Total samples combined: {len(combined_df)}")
    
    # Split data (70% train, 15% validation, 15% test) without stratify due to small 'Clear' class
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)
    
    print(f"Training set size: {len(X_train)}")
    print(f"Validation set size: {len(X_val)}")
    print(f"Test set size: {len(X_test)}")
    
    # Save the splits to standard NumPy formats for easier loading in train_model
    np_dir = os.path.join(DATASET_DIR, "processed")
    os.makedirs(np_dir, exist_ok=True)
    
    import numpy as np
    np.save(os.path.join(np_dir, "X_train.npy"), X_train)
    np.save(os.path.join(np_dir, "y_train.npy"), y_train)
    np.save(os.path.join(np_dir, "X_val.npy"), X_val)
    np.save(os.path.join(np_dir, "y_val.npy"), y_val)
    np.save(os.path.join(np_dir, "X_test.npy"), X_test)
    np.save(os.path.join(np_dir, "y_test.npy"), y_test)
    
    # Extract and save class labels in order
    classes = np.unique(y)
    np.save(os.path.join(np_dir, "classes.npy"), classes)
    
    print("Preprocessing complete. Data saved to dataset/processed/")
    return True

if __name__ == "__main__":
    load_and_preprocess_data()
