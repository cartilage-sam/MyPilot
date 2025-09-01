# 🎙️ AI Interviewer Agent – Complete Guide

Powered by **LiveKit**, **Deepgram**, and **Groq**

## 📌 Overview

The **AI Interviewer Agent** is a real-time **voice-based interview assistant** that:

* Speaks naturally using **Text-to-Speech (TTS)**
* Listens to candidates using **Speech-to-Text (STT)**
* Asks structured **AI/ML interview questions**
* Saves **live transcripts (JSON)** and **final transcripts (TXT)**
* Runs in **low latency real-time rooms** powered by **LiveKit Agents**

This makes it ideal for:

* **Automated technical interviews**
* **Mock interview platforms**
* **Recruitment AI assistants**

---

## ⚙️ Features

* 🔊 **Voice conversation** with candidates
* 📄 **Automatic transcript storage** in JSON + TXT
* 🎯 **Customizable interview questions**
* 🧠 **Groq-powered LLM** for fast AI responses
* 🎙️ **Deepgram Nova-3 STT** for transcription
* 🗣️ **Deepgram Aura TTS** for natural voice output
* 🎚️ **Noise cancellation** & **Voice activity detection (VAD)**

---

## 🚀 Setup & Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/ai-interviewer.git
cd ai-interviewer
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt**

```txt
livekit-agents
python-dotenv
deepgram-sdk
groq
watchdog
```

### 3️⃣ Set Environment Variables

Create a `.env` file:

```env
# LiveKit Server
LIVEKIT_URL=ws://localhost:7880
LIVEKIT_API_KEY=your_api_key
LIVEKIT_API_SECRET=your_api_secret

# Deepgram
DEEPGRAM_API_KEY=your_deepgram_api_key

# Groq
GROQ_API_KEY=your_groq_api_key
```

### 4️⃣ Run the Agent

```bash
python interview_agent.py console
```

You’ll see:

```
📁 Running from: /path/to/project
==================================================
     Livekit Agents - Console
==================================================
Press [Ctrl+B] to toggle between Text/Audio mode, [Q] to quit.
```

---

## 🖥️ Using in Interview Module

### 🔹 Backend Integration

If you’re building an **interview backend service**:

* Keep this agent running as a **LiveKit Worker**
* Expose candidate sessions through **LiveKit Rooms**
* Store transcripts in **your database** by reading from `transcripts_live.json` or `transcripts.txt`

**Example Workflow (Backend):**

1. Candidate joins LiveKit room via your app.
2. This agent joins the same room.
3. Agent conducts the interview.
4. Transcript is stored → send to backend DB.
5. HR/Admin can later review transcript.

### 🔹 Frontend Integration

If you’re building a **React/Next.js frontend**:

* Use **LiveKit’s JS SDK** (`@livekit/client`) to connect candidates to rooms.
* Agent already runs on backend → candidate just talks & listens in real-time.

**React Snippet (Frontend):**

```javascript
import { Room, connect } from "livekit-client";

const room = await connect(LIVEKIT_URL, LIVEKIT_TOKEN);
room.on("trackSubscribed", (track, publication, participant) => {
  if (track.kind === "audio") {
    const audio = new Audio();
    audio.srcObject = new MediaStream([track.mediaStreamTrack]);
    audio.play();
  }
});
```

---

## ☁️ Deployment Guide

### 🔹 Local Deployment

Run **LiveKit Server** locally with Docker:

```bash
docker run --rm -it -p 7880:7880 \
  -e LIVEKIT_API_KEY=devkey \
  -e LIVEKIT_API_SECRET=secret \
  livekit/livekit-server \
  --dev
```

Then run:

```bash
python interview_agent.py console
```

### 🔹 Cloud Deployment (Production)

1. **Deploy LiveKit Server**

   * Use [LiveKit Cloud](https://livekit.io/cloud) (managed)
   * Or self-host with Kubernetes/Docker Compose

2. **Deploy AI Interviewer Worker**

   * Package this script into a container:

   ```dockerfile
   FROM python:3.10
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["python", "interview_agent.py"]
   ```

   * Deploy on **AWS ECS**, **GCP Cloud Run**, or **Kubernetes**

3. **Frontend Client**

   * Use **LiveKit JS SDK** or **LiveKit React SDK**
   * Provide candidates with **room access tokens** generated via your backend

---

## 📂 Transcript Handling

* **Live JSON updates:** `transcripts_live.json`
* **Final transcript (when session closes):** `transcripts.txt`

Example JSON:

```json
[
  {"user": "My experience is with TensorFlow and PyTorch."},
  {"agent": "Can you describe a project you've worked on?"}
]
```

---

## 🛠️ Customization

* Add/remove questions in `must_ask` & `other_than_fields`
* Change LLM model (Groq → OpenAI, Anthropic, etc.)
* Replace Deepgram with another STT/TTS provider

---

## 📚 References

* [LiveKit Agents Docs](https://docs.livekit.io/agents/)
* [LiveKit SDKs](https://docs.livekit.io/client-sdk-js/)
* [Deepgram STT](https://developers.deepgram.com/)
* [Groq LLM](https://groq.com/)

---

✅ With this setup, you now have a **real-time AI Interviewer** that can run locally, integrate into your backend/frontend, and scale to production deployment.
