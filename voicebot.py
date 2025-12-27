import sounddevice as sd
import vosk
import json
import queue
import pyttsx3
import threading

# ------------------------------
# 1. Settings
# ------------------------------
MODEL_PATH = r"C:\Users\admin\Desktop\ai\vosk-model-small-en-us-0.15"
SAMPLE_RATE = 16000
DEBUG = True  # Set True to see recognition debug messages

# ------------------------------
# 2. Load Vosk model
# ------------------------------
model = vosk.Model(MODEL_PATH)
recognizer = vosk.KaldiRecognizer(model, SAMPLE_RATE)

# ------------------------------
# 3. TTS setup
# ------------------------------
speech_queue = queue.Queue()
engine = pyttsx3.init()

def tts_worker():
    """Background TTS worker to speak messages from queue."""
    while True:
        text = speech_queue.get()
        engine.say(text)
        engine.runAndWait()
        speech_queue.task_done()

threading.Thread(target=tts_worker, daemon=True).start()

def speak(text):
    """Add text to queue for speech output."""
    speech_queue.put(text)

# ------------------------------
# 4. Agriculture responses
# ------------------------------
def get_response(text):
    text = text.lower()

    if "weather" in text:
        return "Today's weather looks normal with no major alerts."

    if "fertilizer" in text:
        return "Urea and potash are commonly used fertilizers. Apply in correct proportion."

    if "soil" in text:
        return "Loamy soil is the best soil for agriculture."

    if "paddy" in text:
        return "Paddy cultivation requires standing water of around five centimeters."

    if "groundnut" in text:
        return "Groundnut grows well in sandy loam soil."

    if "hello" in text or "hi" in text:
        return "Hello farmer, how can I help you today?"
    if "stop" in text:
        return "Okay, stopping for now."

    return "Sorry, I did not understand."

# ------------------------------
# 5. Microphone callback
# ------------------------------
def callback(indata, frames, time, status):
    audio_data = bytes(indata)

    if recognizer.AcceptWaveform(audio_data):
        result = json.loads(recognizer.Result())
        text = result.get("text", "")

        if DEBUG:
            print("Recognized:", text)

        if text.strip() != "":
            response = get_response(text)
            if DEBUG:
                print("Speaking:", response)
            speak(response)

# ------------------------------
# 6. Start the bot
# ------------------------------
try:
    with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        speak("Hello, I am your agriculture assistant.")  # Greeting
        while True:
            pass
except KeyboardInterrupt:
    print("\nExiting...")
