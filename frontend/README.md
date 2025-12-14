# TV Monitor Agent – Live Feed Transcription & Summarization

## Overview

This project is a **Monitor Agent prototype** that continuously monitors a live TV stream, extracts audio, generates **1‑minute transcripts**, and produces **short AI summaries** for each segment. The system is designed to work **near real‑time**, with robustness against local resource limitations.

The prototype was built as part of a technical assignment to demonstrate:

* Live stream processing
* Audio extraction
* Speech‑to‑text transcription
* AI‑assisted summarization
* A simple frontend for monitoring and control

---

## Features

* 🎥 Live TV feed ingestion using **FFmpeg**
* 🔊 Continuous audio extraction
* 📝 Transcription every **1 minute** using **OpenAI Whisper (local)**
* 🧠 AI summarization (≤ 15 words per segment)

  * Local LLM via **Ollama (phi model)**
  * Automatic **fallback extractive summary** if LLM fails
* ⏯️ Start / Stop monitoring controls
* 📊 Frontend dashboard showing:

  * Timestamp
  * Video time window
  * Full transcript
  * AI summary

---

## Tech Stack

### Backend

* Python 3.11
* FastAPI
* Uvicorn
* FFmpeg
* Whisper (speech‑to‑text)
* Ollama (local LLM)

### Frontend

* React (Vite)
* Plain CSS

---

## Project Structure

```
AI Summarizer/
├── backend/
│   ├── main.py          # FastAPI app & monitor loop
│   ├── capture.py       # Live stream audio capture (FFmpeg)
│   ├── transcribe.py    # Whisper transcription logic
│   ├── processor.py    # AI summarization + fallback logic
│   ├── storage.py      # In‑memory storage for records
│   ├── config.py       # Stream & timing configuration
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   ├── index.html
│   └── package.json
│
└── README.md
```

---

## Setup Instructions

### 1️⃣ Prerequisites

* Python **3.11** installed
* Node.js **18+** installed
* FFmpeg installed and added to PATH
* Ollama installed

Verify installations:

```bash
python --version
node --version
ffmpeg -version
```

---

### 2️⃣ Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Start the backend:

```bash
python -m uvicorn main:app --reload
```

Backend runs at:

```
http://127.0.0.1:8000
```

---

### 3️⃣ Ollama Setup (Local LLM)

Pull the model:

```bash
ollama pull phi
```

Verify:

```bash
ollama list
```

The project uses:

```
phi:latest
```

---

### 4️⃣ Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at:

```
http://localhost:5173
```

---

## How It Works

1. User clicks **Start Monitoring**
2. Backend starts a background thread
3. Every 1 minute:

   * Audio is extracted from the live stream
   * Whisper generates a transcript
   * Transcript is summarized:

     * First via local LLM (Ollama)
     * If LLM fails → deterministic extractive fallback
4. Result is stored and exposed via `/data`
5. Frontend polls `/data` and updates the UI

---

## Reliability Design

* **Input truncation** prevents LLM crashes on long transcripts
* **Fallback summarization** guarantees output even if LLM fails
* Guard against multiple monitoring threads
* Designed for CPU‑only environments

This ensures the system never breaks during live monitoring.

---

## Performance Notes

* Processing is done in **fixed 1‑minute windows**
* Small delay (≈ 1 minute) is expected by design
* Optimized for stability rather than low‑latency streaming

---

## Known Limitations

* Local LLM performance depends on CPU resources
* Not intended for high‑throughput production use
* In‑memory storage (data resets on restart)

---

## Future Improvements

* Persistent database storage
* GPU‑accelerated inference
* Multi‑channel stream support
* Keyword alerts and topic detection
* Authentication and user management

---

## Summary

This prototype demonstrates an end‑to‑end **live media monitoring system** with real‑time transcription and AI summarization, focusing on **robustness, clarity, and practical engineering trade‑offs**.

---

**Author:** Vedhavathi Kosuri
