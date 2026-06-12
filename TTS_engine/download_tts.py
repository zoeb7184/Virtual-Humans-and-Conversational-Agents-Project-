import requests
import os

print(" Downloading Kokoro TTS models... this might take 1-2 minutes.")

# URLs for the model files (hosted on GitHub Releases for speed)
MODEL_URL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files/kokoro-v0_19.onnx"
VOICES_URL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files/voices.json"

def download_file(url, filename):
    if os.path.exists(filename):
        print(f" {filename} already exists.")
        return
    print(f" Downloading {filename}...")
    response = requests.get(url, stream=True)
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f" Saved {filename}")

download_file(MODEL_URL, "kokoro-v0_19.onnx")
download_file(VOICES_URL, "voices.json")

print("\n🎉 Download complete! You can now delete this script.")