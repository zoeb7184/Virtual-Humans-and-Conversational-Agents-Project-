print("1. Starting Python...")
import sys
print("2. System loaded.")

print("3. Importing Requests...")
import requests
print("4. Requests imported.")

print("5. Importing Numpy...")
import numpy
print("6. Numpy imported.")

print("7. Importing SoundDevice...")
import sounddevice as sd
print("8. SoundDevice imported.")

print("9. Importing Faster-Whisper (This is usually the slow part)...")
from faster_whisper import WhisperModel
print("10. Faster-Whisper imported!")

print("✅ SUCCESS: All libraries are working.")