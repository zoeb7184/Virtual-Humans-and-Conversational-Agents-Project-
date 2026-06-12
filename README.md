# Voice-Controlled Robotic Manipulation System

### Hybrid Cloud-Edge Conversational AI using Whisper Large-v3, Rasa NLU, ROS2, and Kokoro TTS

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Rasa](https://img.shields.io/badge/Rasa-Conversational%20AI-purple)
![ROS2](https://img.shields.io/badge/ROS2-Robotics-green)
![Whisper](https://img.shields.io/badge/Whisper-Large--v3-red)
![Architecture](https://img.shields.io/badge/Architecture-Cloud%2FEdge%20Hybrid-orange)

A real-time voice-controlled robotic manipulation system that combines cloud-based speech recognition with local ROS2 robotic control to enable natural language interaction with a robotic arm. The system supports object manipulation tasks such as pick-and-place operations, object handovers, and spatial placement commands through conversational voice commands.

---

## 🎥 Demo

https://github.com/zoeb7184/Virtual-Humans-and-Conversational-Agents-Project-/blob/main/Docs/demo_video.mp4

The robotic arm can understand and execute commands such as:

* "Pick-up the tamato. (As shown in the video)"
* "Put the small box behind the lemon."
* "Give me the yellow lemon."
* "Give me all lemons."
* "Stop."
* "Let's try again."

---

## 🚀 The Challenge & Solution

### The Problem

Running state-of-the-art Automatic Speech Recognition (ASR) models such as Whisper Large-v3 locally on a CPU introduces significant latency (up to 12 seconds), making responsive voice-controlled robotic manipulation difficult.

### The Solution

To overcome this limitation, a hybrid cloud-edge architecture was developed.

Heavy speech recognition workloads are offloaded to a Google Colab T4 GPU through a secure Cloudflare Tunnel, while conversational reasoning, robotic control, and speech synthesis remain on the local machine. This architecture dramatically reduces latency while maintaining reliable robotic control.

---

## 🏗️ System Architecture

![Voice-Controlled Robotic Manipulation System](Docs/architecture_diagram.png)

*Figure 1. Hybrid cloud-edge architecture integrating Whisper Large-v3, Rasa NLU, ROS2, Cloudflare Tunnel, and Kokoro TTS.*

This system combines cloud-based speech recognition with local robotic manipulation to enable natural language control of a robotic arm.

### Processing Pipeline

1. **Voice Command Acquisition** – User speech is captured through a local microphone.
2. **Cloud-Based Speech Recognition** – Audio is securely transmitted via Cloudflare Tunnel to a cloud-hosted Whisper Large-v3 model.
3. **Natural Language Understanding** – Rasa NLU extracts intents, objects, attributes, and spatial relationships.
4. **Task Planning** – Commands are translated into structured robotic manipulation actions.
5. **Robotic Arm Execution** – ROS2 control nodes execute pick-and-place and handover tasks.
6. **Speech Feedback** – Kokoro TTS generates spoken confirmations and responses.

---

## 📊 Results

| Configuration       | ASR Latency  |
| ------------------- | ------------ |
| Local CPU           | ~12 seconds  |
| Google Colab T4 GPU | ~1–2 seconds |

**Performance Improvement:** 6–10× faster transcription compared to local CPU execution.

---

## 🗣️ Supported Voice Commands

### Greetings

* Hello
* Hi
* Hello robot
* Hi system
* Hello Hal

### Place Commands

* Put the red apple on the table
* Put the small box behind the lemon
* Put all bananas in the box
* Put the green sphere left of the stone
* Put the white box onto the table

### Give Commands

* Give me the red apple
* Give me a banana
* Give me all lemons
* Give me the purple stone

### Control Commands

* Stop
* Halt
* Freeze
* Let's try again
* Yes
* No

---

## 📂 Repository Structure

```text
Virtual-Humans-and-Conversational-Agents-Project-
│
├── Core_scripts/
├── Rasa_bot/
├── TTS_engine/
└── Docs/
    ├── architecture_diagram.png
    ├── demo_video.mp4
    └── Voice Robot Command Cheat Sheet
```

### Folder Overview

| Folder       | Purpose                                                  |
| ------------ | -------------------------------------------------------- |
| Core_scripts | Robot control, execution logic, and cloud communication  |
| Rasa_bot     | Conversational AI and intent recognition                 |
| TTS_engine   | Kokoro Text-to-Speech configuration                      |
| Docs         | Documentation, architecture diagrams, and demonstrations |

---

## 🛠️ Installation & Setup

### Clone Repository

```bash
git clone https://github.com/zoeb7184/Virtual-Humans-and-Conversational-Agents-Project-.git
cd Virtual-Humans-and-Conversational-Agents-Project-
```

### Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🎤 Download Kokoro TTS Models

```bash
cd TTS_engine
python download_tts.py
```

If required:

```bash
python fix_download.py
```

---

## ☁️ Cloud GPU Setup

1. Open the Google Colab notebook.
2. Enable a T4 GPU runtime.
3. Run all notebook cells.
4. Start Cloudflare Tunnel.
5. Copy the generated endpoint URL.
6. Update the local configuration.

---

## 💻 Running the System

### Terminal 1 – Rasa Action Server

```bash
cd Rasa_bot
rasa run actions
```

### Terminal 2 – Rasa Core

```bash
cd Rasa_bot
rasa run --enable-api
```

### Terminal 3 – Robot Controller

```bash
cd Core_scripts
python robot_main.py
```

---

## 🧰 Technology Stack

* Python
* ROS2
* Rasa Open Source
* Whisper Large-v3
* Google Colab T4 GPU
* Cloudflare Tunnel
* Kokoro TTS
* Hybrid Cloud-Edge Computing

---

## 🔍 Skills Demonstrated

* Conversational AI
* Speech Recognition (ASR)
* Natural Language Understanding
* Human-Robot Interaction
* Robotic Manipulation
* ROS2 Development
* Distributed Systems
* Cloud Computing
* Edge AI
* Python Development

---

## 👨‍💻 Author

### Zoeb Ali Khan

* GitHub: https://github.com/zoeb7184
* LinkedIn: https://linkedin.com/in/zoeb-ali-khan

---

## 📄 License

Developed as part of the Virtual Humans & Conversational Agents coursework, focusing on conversational AI and robotic manipulation systems.
