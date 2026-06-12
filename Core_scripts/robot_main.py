import requests
import sounddevice as sd
import soundfile as sf
import numpy as np
from faster_whisper import WhisperModel
from kokoro_onnx import Kokoro
import time

# --- CONFIGURATION ---
RASA_URL = "http://localhost:5005/webhooks/rest/webhook"
SAMPLING_RATE = 16000
DURATION = 5  # Listen duration
ASR_MODEL_SIZE = "tiny" 

# --- INITIALIZE WHISPER (EARS) ---
print(f"Loading Faster-Whisper ({ASR_MODEL_SIZE})...")
asr_model = WhisperModel(ASR_MODEL_SIZE, device="cpu", compute_type="int8")
print("Whisper Loaded.")

# --- INITIALIZE KOKORO (MOUTH) ---
print("Loading Kokoro TTS (v1.0)...")
try:
    # UPDATED: Using v1.0 filenames
    tts_model = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")
    VOICE_NAME = "af_sarah" 
    print("Kokoro Loaded.")
except Exception as e:
    print(f"Error loading Kokoro: {e}")
    exit()

def record_audio(duration):
    print(f"\nListening for {duration} seconds...")
    audio = sd.rec(int(duration * SAMPLING_RATE), samplerate=SAMPLING_RATE, channels=1, dtype='float32')
    sd.wait()
    print("Recording stopped.")
    return audio.flatten()

def transcribe(audio_data):
    print("Transcribing...")
    segments, _ = asr_model.transcribe(audio_data, beam_size=5)
    text = " ".join([segment.text for segment in segments]).strip()
    return text

def talk_to_rasa(text):
    if not text:
        return None
    
    print(f"Sending to Brain: '{text}'")
    payload = {"sender": "user", "message": text}
    try:
        response = requests.post(RASA_URL, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error connecting to Rasa: {e}")
        return []

def speak_text(text):
    print(f"🔊 Generating Audio: '{text}'")
    # Generate audio from text
    # speed=1.0 is normal, 1.2 is faster robot
    samples, sample_rate = tts_model.create_audio(text, voice=VOICE_NAME, speed=1.0)
    
    # Play the audio
    sd.play(samples, sample_rate)
    sd.wait() # Wait for it to finish talking

# --- MAIN LOOP ---
def main():
    print("\nROBOT IS READY. TALK TO ME!")
    while True:
        try:
            input("\nPress Enter to speak (or Ctrl+C to exit)...")
            
            # 1. Listen
            audio_data = record_audio(DURATION)
            
            # 2. Transcribe
            user_text = transcribe(audio_data)
            print(f"🗣️ You said: {user_text}")
            
            if not user_text:
                print("I didn't hear anything.")
                continue

            # 3. Understand (Brain)
            bot_responses = talk_to_rasa(user_text)
            
            # 4. Speak (Mouth)
            for resp in bot_responses:
                if 'text' in resp:
                    bot_text = resp['text']
                    print(f"🤖 Bot Text: {bot_text}")
                    speak_text(bot_text)
                    
        except KeyboardInterrupt:
            print("\nShutting down...")
            break

if __name__ == "__main__":
    main()