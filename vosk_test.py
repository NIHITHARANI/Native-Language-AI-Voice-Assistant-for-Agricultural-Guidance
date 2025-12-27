from vosk import Model, KaldiRecognizer
import wave
import json

model = Model(r"C:\Users\admin\Desktop\ai\vosk-model-small-en-us-0.15")
wf = wave.open("test.wav", "rb")
rec = KaldiRecognizer(model, wf.getframerate())

while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        result = json.loads(rec.Result())
        print("Recognized:", result.get("text", ""))
