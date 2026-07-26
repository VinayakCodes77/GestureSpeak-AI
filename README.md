# GestureSpeak AI 🤖🤟

**GestureSpeak AI** is a Real-time American Sign Language (ASL) Recognition System built for assisting communication between deaf or mute individuals and non-sign-language users. 

This project utilizes **Google MediaPipe** for robust 3D hand tracking and a high-performance **Deep Neural Network (MLP)** for real-time classification, achieving **>99% accuracy**.

## 🌟 Key Features
- **Real-Time Detection:** Live webcam inference processing 3D hand landmarks instantly.
- **Full ASL Alphabet (A-Z):** Supports all 26 English letters.
- **Intelligent Text Generation:** Includes smart debouncing and cooldown algorithms to prevent duplicate letter spamming, ensuring clean sentence construction.
- **Special Commands:** Built-in gestures for `SPACE`, `DELETE`, and `CLEAR` to give users full control over their sentences.
- **Text-to-Speech (TTS):** Integrated offline voice synthesis to speak the generated sentences out loud at the click of a button.
- **High Accuracy Filtering:** Enforces a strict >85% confidence threshold to ignore blurry or uncertain frames.

## 🛠️ Technology Stack
- **Python 3.12**
- **OpenCV:** Real-time webcam capture and image processing.
- **Google MediaPipe:** Extraction of 21 3D hand landmarks (63 total features).
- **Scikit-Learn (MLPClassifier):** Deep learning model for gesture classification.
- **CustomTkinter:** Modern, responsive Graphical User Interface (GUI).
- **pyttsx3:** Offline Text-to-Speech engine.
- **Pandas & NumPy:** Data preprocessing and CSV manipulation.

## 📁 Project Structure
```text
GestureSpeakAI/
│
├── dataset/
│   ├── processed/      # Contains normalized .npy arrays for training/testing
│   └── train/          # Contains raw extracted .csv landmarks for every gesture
│
├── models/
│   ├── gesture_model.pkl    # The compiled Neural Network weights
│   ├── label_encoder.pkl    # Class label mappings
│   ├── confusion_matrix.png # Visual training evaluation
│
├── src/
│   ├── collect_dataset.py                 # Script to record new webcam datasets
│   ├── extract_landmarks_from_images.py   # Script to extract landmarks from raw images
│   ├── preprocess_data.py                 # Data normalization and splitting pipeline
│   ├── train_model.py                     # Compiles and trains the MLP Neural Network
│   ├── predict.py                         # Inference engine for the GUI
│   ├── speech.py                          # TTS Engine integration
│   ├── utils.py                           # MediaPipe initialization and math utilities
│   └── gui.py                             # CustomTkinter dashboard
│
└── main.py                                # Application entry point
```

## 🚀 How to Run
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Launch the Application:
```bash
python main.py
```

## 🧠 Training Your Own Model
If you want to map the system to your own hands or add new custom commands:
1. Run `python src/collect_dataset.py` to launch the data collector.
2. Follow the on-screen prompts to record your gestures.
3. Run `python src/preprocess_data.py` to normalize the data.
4. Run `python src/train_model.py` to recompile the neural network.

---
*Built as a B.Tech Project focusing on Accessibility and Machine Learning.*
