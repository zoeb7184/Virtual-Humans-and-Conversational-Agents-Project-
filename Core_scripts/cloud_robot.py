import sounddevice as sd
import soundfile as sf
import requests
import numpy as np
import io
import sys

# --- CONFIGURATION ---
# 1. PASTE YOUR COLAB URL HERE!
SERVER_URL = "https://oil-planners-contemporary-listing.trycloudflare.com/process_audio" 

SAMPLE_RATE = 16000
DURATION = 4.0 #How long to listen (seconds)

def main():
    print(f"Connecting to Cloud Brain...")
    
    if "PASTE_" in SERVER_URL:
        print("ERROR: You forgot to paste the Cloudflare URL in the script!")
        return

    print("System Ready. (Using Tesla T4 GPU in Cloud)")
    print(f"   Target: {SERVER_URL}")
    
    while True:
        try:
            input("\nPress Enter to Speak (4s)...")
            
            # 1. Record
            print("Recording...")
            audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='float32')
            sd.wait()
            print("Sending to Cloud...")

            # 2. Convert to WAV
            wav_buffer = io.BytesIO()
            sf.write(wav_buffer, audio, SAMPLE_RATE, format='WAV')
            wav_buffer.seek(0)

            # 3. Send to Colab
            files = {'audio': ('command.wav', wav_buffer, 'audio/wav')}
            
            # 30 second timeout because the first run in Cloud can be slow
            response = requests.post(SERVER_URL, files=files, timeout=30)

            # 4. Handle Response
            if response.status_code == 200:
                print("Playing Reply...")
                audio_data = io.BytesIO(response.content)
                data, samplerate = sf.read(audio_data)
                sd.play(data, samplerate)
                sd.wait()
            else:
                print(f"Server Error ({response.status_code}):")
                print(response.text)
                
        except KeyboardInterrupt:
            print("\nStopping...")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
