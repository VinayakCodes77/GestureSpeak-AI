import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
import time
from src.utils import init_mediapipe_hands, extract_landmarks, draw_landmarks
from src.predict import GesturePredictor
from src.speech import SpeechEngine

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("GestureSpeak AI")
        self.geometry("1000x600")

        # Initialize core components
        self.hands = init_mediapipe_hands()
        self.predictor = GesturePredictor()
        self.speech_engine = SpeechEngine()
        self.cap = None
        self.is_running = False

        self.current_sentence = ""
        self.last_predicted_char = ""
        self.prediction_confidence = 0.0
        self.frames_since_last_action = 0
        self.action_cooldown = 30 # roughly 1 second at 30 fps
        self.last_added_char = ""
        
        # Stability tracking
        self.current_pending_char = ""
        self.pending_char_frames = 0
        self.required_stable_frames = 10 # Must hold the sign for ~10 frames (~0.33s) before it registers

        self._setup_ui()

    def _setup_ui(self):
        # Grid layout
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Video Frame
        self.video_frame = ctk.CTkFrame(self)
        self.video_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.video_frame.grid_rowconfigure(0, weight=1)
        self.video_frame.grid_columnconfigure(0, weight=1)
        
        self.video_label = ctk.CTkLabel(self.video_frame, text="")
        self.video_label.grid(row=0, column=0, padx=5, pady=5)

        # Control Panel
        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="nsew")

        # Prediction Display
        self.pred_label_title = ctk.CTkLabel(self.control_frame, text="Current Prediction:", font=("Arial", 16, "bold"))
        self.pred_label_title.pack(pady=(20, 5))
        
        self.pred_char_label = ctk.CTkLabel(self.control_frame, text="-", font=("Arial", 60, "bold"), text_color="#00a8ff")
        self.pred_char_label.pack(pady=5)
        
        self.conf_progressbar = ctk.CTkProgressBar(self.control_frame)
        self.conf_progressbar.pack(pady=5, padx=20)
        self.conf_progressbar.set(0)
        
        self.conf_label = ctk.CTkLabel(self.control_frame, text="Confidence: 0%")
        self.conf_label.pack(pady=(0, 20))

        # Sentence Display
        self.sentence_label_title = ctk.CTkLabel(self.control_frame, text="Sentence:", font=("Arial", 16, "bold"))
        self.sentence_label_title.pack(pady=(10, 5))
        
        self.sentence_textbox = ctk.CTkTextbox(self.control_frame, height=100, font=("Arial", 14))
        self.sentence_textbox.pack(padx=20, pady=5, fill="x")
        self.sentence_textbox.insert("0.0", "")
        self.sentence_textbox.configure(state="disabled")

        # Buttons
        self.btn_frame = ctk.CTkFrame(self.control_frame, fg_color="transparent")
        self.btn_frame.pack(pady=20, fill="x", padx=20)
        
        self.start_btn = ctk.CTkButton(self.btn_frame, text="Start Camera", command=self.toggle_camera)
        self.start_btn.pack(side="left", expand=True, padx=5)
        
        self.speak_btn = ctk.CTkButton(self.btn_frame, text="Speak", command=self.speak_sentence)
        self.speak_btn.pack(side="right", expand=True, padx=5)
        
        self.clear_btn = ctk.CTkButton(self.control_frame, text="Clear Sentence", command=self.clear_sentence)
        self.clear_btn.pack(pady=10)

        # FPS Display
        self.fps_label = ctk.CTkLabel(self.control_frame, text="FPS: 0", text_color="gray")
        self.fps_label.pack(side="bottom", pady=10)
        
        self.prev_time = 0

    def toggle_camera(self):
        if not self.is_running:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                print("Failed to open camera.")
                return
            self.is_running = True
            self.start_btn.configure(text="Stop Camera")
            self.update_frame()
        else:
            self.is_running = False
            self.start_btn.configure(text="Start Camera")
            if self.cap:
                self.cap.release()
            self.video_label.configure(image="")

    def update_frame(self):
        if not self.is_running:
            return

        success, image = self.cap.read()
        if success:
            # Calculate FPS
            curr_time = time.time()
            fps = 1 / (curr_time - self.prev_time) if self.prev_time > 0 else 0
            self.prev_time = curr_time
            self.fps_label.configure(text=f"FPS: {int(fps)}")

            # Flip and process image
            image = cv2.flip(image, 1)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = self.hands.process(image_rgb)

            self.frames_since_last_action += 1

            if results.multi_hand_landmarks and results.multi_handedness:
                for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                    
                    # MediaPipe handedness is flipped because we used cv2.flip(image, 1) earlier
                    # So MediaPipe "Left" actually means the user's physical Right hand
                    detected_hand = handedness.classification[0].label
                    physical_hand = "Right" if detected_hand == "Left" else "Left"

                    draw_landmarks(image_rgb, hand_landmarks)
                    landmarks = extract_landmarks(hand_landmarks)
                    
                    predicted_char, confidence = self.predictor.predict(landmarks)
                    
                    # --- Handedness Filter Logic ---
                    commands = ["Space", "Delete", "Clear"]
                    
                    # If Left hand tries to do a command, ignore it
                    if physical_hand == "Left" and predicted_char in commands:
                        confidence = 0.0 # Force reject
                        predicted_char = f"{predicted_char} (Use Right Hand)"
                        
                    # If Right hand tries to do A-Z, ignore it
                    elif physical_hand == "Right" and predicted_char not in commands:
                        confidence = 0.0 # Force reject
                        predicted_char = f"{predicted_char} (Use Left Hand)"
                    
                    self.last_predicted_char = predicted_char
                    self.prediction_confidence = confidence
                    
                    # Update Prediction UI
                    self.pred_char_label.configure(text=f"{predicted_char}")
                    self.conf_progressbar.set(confidence)
                    self.conf_label.configure(text=f"Confidence: {int(confidence*100)}%")

                    # Enforce strictly > 85% confidence and debounce logic
                    if confidence > 0.85:
                        if predicted_char == self.current_pending_char:
                            self.pending_char_frames += 1
                        else:
                            self.current_pending_char = predicted_char
                            self.pending_char_frames = 1
                            
                        # If the sign has been held steadily for the required frames
                        if self.pending_char_frames >= self.required_stable_frames:
                            # Add only if it's a different character OR enough time has passed
                            if predicted_char != self.last_added_char or self.frames_since_last_action > self.action_cooldown:
                                self.process_prediction(predicted_char)
                                self.last_added_char = predicted_char
                                self.frames_since_last_action = 0
                                self.pending_char_frames = 0 # Reset so it doesn't double-trigger
                    else:
                        # Reset stability if confidence drops
                        self.pending_char_frames = 0
                        self.current_pending_char = ""
                    
                    # Only process one hand
                    break
            else:
                self.pred_char_label.configure(text="-")
                self.conf_progressbar.set(0)
                self.conf_label.configure(text="Confidence: 0%")

            # Convert to PIL Image and then to ImageTk
            img = Image.fromarray(image_rgb)
            imgtk = ctk.CTkImage(light_image=img, dark_image=img, size=(640, 480))
            self.video_label.configure(image=imgtk)
            self.video_label.image = imgtk

        self.after(15, self.update_frame)

    def process_prediction(self, char):
        if char == "Space":
            self.current_sentence += " "
        elif char == "Delete":
            self.current_sentence = self.current_sentence[:-1]
        elif char == "Clear":
            self.current_sentence = ""
        else:
            self.current_sentence += char
            
        self.update_sentence_ui()

    def update_sentence_ui(self):
        self.sentence_textbox.configure(state="normal")
        self.sentence_textbox.delete("0.0", "end")
        self.sentence_textbox.insert("0.0", self.current_sentence)
        self.sentence_textbox.configure(state="disabled")

    def clear_sentence(self):
        self.current_sentence = ""
        self.update_sentence_ui()

    def speak_sentence(self):
        if self.current_sentence.strip():
            self.speech_engine.speak(self.current_sentence)

    def on_closing(self):
        self.is_running = False
        if self.cap:
            self.cap.release()
        self.destroy()
