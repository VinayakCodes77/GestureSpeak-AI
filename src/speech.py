import pyttsx3
import threading

class SpeechEngine:
    def __init__(self):
        self.is_speaking = False
        
    def speak(self, text):
        """Speaks the text in a non-blocking background thread."""
        if self.is_speaking or not text:
            return
            
        def _speak_thread():
            self.is_speaking = True
            try:
                # Need to re-init in thread on some platforms, but usually works if engine is thread-safe
                # For Windows pyttsx3, creating a new instance per thread is safer.
                local_engine = pyttsx3.init()
                local_engine.say(text)
                local_engine.runAndWait()
            except Exception as e:
                print(f"Speech error: {e}")
            finally:
                self.is_speaking = False
                
        threading.Thread(target=_speak_thread, daemon=True).start()
