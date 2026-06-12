import requests
import os
import sys

# Define filenames
FILES = {
    "kokoro-v0_19.onnx": "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files/kokoro-v0_19.onnx",
    "voices.json": "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files/voices.json"
}

def download_file(url, filename):
    # 1. DELETE existing file to force fresh download
    if os.path.exists(filename):
        print(f"🗑️  Deleting corrupt {filename}...")
        os.remove(filename)

    print(f"⬇️  Downloading {filename}...")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status() # Check for 404 errors
        
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024 # 1 Kilobyte
        
        with open(filename, 'wb') as f:
            downloaded = 0
            for chunk in response.iter_content(chunk_size=block_size):
                f.write(chunk)
                downloaded += len(chunk)
                # Simple progress bar
                if total_size > 0:
                    percent = int(50 * downloaded / total_size)
                    sys.stdout.write(f"\r[{'=' * percent}{' ' * (50-percent)}] {int(downloaded/1024)} KB")
                    sys.stdout.flush()
        
        print(f"\n Saved {filename} ({os.path.getsize(filename) // 1024} KB)")
        
    except Exception as e:
        print(f"\n Failed to download {filename}: {e}")

# Run the downloads
for name, link in FILES.items():
    download_file(link, name)

print("\n🎉 Repair Complete! Now try running robot_main.py again.")