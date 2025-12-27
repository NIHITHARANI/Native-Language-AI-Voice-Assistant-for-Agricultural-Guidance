import sounddevice as sd

def callback(indata, frames, time, status):
    print("🎤 Captured audio chunk!")  # This prints when mic detects sound

with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                       channels=1, callback=callback):
    print("Listening... Speak into your microphone!")
    import time
    while True:
        time.sleep(1)
