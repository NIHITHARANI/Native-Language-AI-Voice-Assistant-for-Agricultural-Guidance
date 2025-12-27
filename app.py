from flask import Flask, render_template, request, jsonify
import vosk
import json
import pyttsx3

# ------------------------------
# Flask setup
# ------------------------------
app = Flask(__name__)

# ------------------------------
# Load Vosk model
# ------------------------------
model = vosk.Model(r"C:\Users\admin\Desktop\ai\vosk-model-small-en-us-0.15")
recognizer = vosk.KaldiRecognizer(model, 16000)

# ------------------------------
# TTS setup
# ------------------------------
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# ------------------------------
# Agriculture responses
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
    return "Sorry, I did not understand."

# ------------------------------
# Routes
# ------------------------------
@app.route('/')
def index():
    return render_template("index.html")  # Web page

@app.route('/ask', methods=['POST'])
def ask():
    text = request.form['text']
    response = get_response(text)
    speak(response)  # speak in server machine
    return jsonify({"response": response})

# ------------------------------
if __name__ == "__main__":
    app.run(debug=True)
