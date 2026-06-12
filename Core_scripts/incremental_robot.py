import queue
import sys
import sounddevice as sd
import numpy as np
import requests
import time
from faster_whisper import WhisperModel
from kokoro_onnx import Kokoro

# --- CONFIGURATION ---
RASA_URL = "http://localhost:5005/model/parse"
SAMPLE_RATE = 16000
CHUNK_DURATION = 1.0 
PAUSE_THRESHOLD = 2.0

# --- UPGRADE: DISTIL-WHISPER ---
# This is the "Magic" model. 
# It is 'Medium' intelligence but stripped down to run 600% faster.
# Perfect for MacBook Air CPU.
MODEL_SIZE = "Systran/faster-distil-whisper-medium.en"

msg_queue = queue.Queue()

# --- LOAD MODELS ---
print(f"⏳ Loading Distilled Model ({MODEL_SIZE})...")
print("   (This downloads ~700MB. It handles accents/noise much better than Small)")
try:
    # compute_type="int8" is crucial for Mac CPU performance
    asr_model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")
    tts_model = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")
    print("✅ Models Loaded.")
except Exception as e:
    print(f"❌ Model Error: {e}")
    sys.exit(1)

def audio_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    msg_queue.put(indata.copy())

def speak(text):
    print(f"🔊 Robot Speaking: '{text}'")
    try:
        samples, sample_rate = tts_model.create(text, voice="af_sarah", speed=1.0, lang="en-us")
        sd.play(samples, sample_rate)
        sd.wait()
    except Exception as e:
        print(f"❌ TTS Error: {e}")

def get_robot_command(text):
    print(f"   ➡️ Analyzing Intent: '{text}'")
    try:
        payload = {"text": text}
        response = requests.post(RASA_URL, json=payload)
        return response.json()
    except Exception as e:
        print(f"❌ Rasa Connection Error: {e}")
        return {}

def main():
    print("🔊 Testing Audio Output...")
    speak("Distil System Online. Fast and Smart.")

    print(f"\n🔴 LIVE: Speak naturally! (Using {MODEL_SIZE})")
    
    audio_buffer = np.array([], dtype='float32')
    last_text = ""
    last_change_time = time.time()
    
    # Context hints to ensure it hears "robot" and "tomato" correctly
    ROBOT_CONTEXT = (
        "hey robot left right agent arm pick up place move to "
        "tomato knife cutting board stop pan bowl cup table object"
    )
    
    with sd.InputStream(channels=1, samplerate=SAMPLE_RATE, callback=audio_callback):
        while True:
            try:
                new_data = msg_queue.get(timeout=0.5)
                new_data = new_data.flatten().astype('float32')
                audio_buffer = np.concatenate((audio_buffer, new_data))
            except queue.Empty:
                pass

            if len(audio_buffer) > SAMPLE_RATE * CHUNK_DURATION:
                
                start_t = time.time()
                
                # OPTIMIZATION:
                segments, _ = asr_model.transcribe(
                    audio_buffer, 
                    beam_size=1, 
                    initial_prompt=ROBOT_CONTEXT, 
                    language="en",
                    vad_filter=True, 
                    # Tweak VAD to stop hearing "hit" (noise)
                    vad_parameters=dict(min_silence_duration_ms=500, threshold=0.5)
                )
                current_text = " ".join([s.text for s in segments]).strip()
                process_time = time.time() - start_t
                
                # Filter hallucinations
                hallucinations = ["thank you", "you", "subs by", "watching", "hit", "audio"]
                if any(h in current_text.lower() for h in hallucinations):
                    current_text = ""
                
                current_text = current_text.replace(".", "").replace("?", "").strip()

                if current_text:
                    # Monitor the Lag. Distil should keep this low.
                    print(f"\r👂 Hearing: {current_text} (Lag: {process_time:.2f}s)   ", end="", flush=True)
                
                if current_text != last_text:
                    last_text = current_text
                    last_change_time = time.time()
                
                # Trigger Logic
                if len(current_text) > 5 and (time.time() - last_change_time > PAUSE_THRESHOLD):
                    
                    print(f"\n\n🚀 SENDING TO BRAIN: {current_text}")
                    
                    data = get_robot_command(current_text)
                    
                    intent = data.get("intent", {}).get("name", "unknown")
                    entities = data.get("entities", [])
                    conf = data.get("intent", {}).get("confidence", 0)
                    
                    if conf < 0.6:
                        speak("I am not sure what you mean.")
                    else:
                        det_agent = "Unknown"
                        det_obj = "Unknown"
                        det_loc = "Unknown"

                        for ent in entities:
                            if ent['entity'] == "agent": det_agent = ent['value']
                            if ent['entity'] == "object": det_obj = ent['value']
                            if ent['entity'] == "location": det_loc = ent['value']

                        # --- ROBOT LOGIC ---
                        if intent == "pick_up":
                            if det_obj != "Unknown":
                                resp = f"Picking up the {det_obj}."
                                if det_agent != "Unknown":
                                    resp = f"{det_agent} agent picking up the {det_obj}."
                                speak(resp)
                            else:
                                speak("What object should I pick up?")
                                
                        elif intent == "move_to":
                            if det_loc != "Unknown":
                                speak(f"Moving to the {det_loc}.")
                            else:
                                speak("Where should I move?")
                                
                        elif intent == "place":
                            if det_loc != "Unknown":
                                speak(f"Placing object on the {det_loc}.")
                            else:
                                speak("Where should I place it?")

                        elif intent == "stop":
                            speak("Stopping immediately.")
                            
                        else:
                            speak("Command not recognized.")
                    
                    # Reset
                    print("\n Listening again...")
                    audio_buffer = np.array([], dtype='float32')
                    last_text = ""
                    last_change_time = time.time()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped.")