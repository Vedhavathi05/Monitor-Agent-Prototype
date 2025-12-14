from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import threading
import time
from datetime import datetime, timedelta

from capture import capture_audio
from transcribe import transcribe_audio
from processor import summarize
from storage import add_record, get_records

app = FastAPI()
running = False

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def monitor():
    global running
    while running:
        start = datetime.now()
        end = start + timedelta(minutes=1)

        capture_audio()
        transcript = transcribe_audio()
        summary = summarize(transcript)

        add_record({
            "timestamp": start.strftime("%Y-%m-%d %H:%M:%S"),
            "video_window": f"{start.strftime('%H:%M:%S')} - {end.strftime('%H:%M:%S')}",
            "transcript": transcript,
            "summary": summary
        })

        time.sleep(60)

@app.post("/start")
def start_monitoring():
    global running
    if not running:
        running = True
        threading.Thread(target=monitor, daemon=True).start()
    return {"status": "Started"}

@app.post("/stop")
def stop_monitoring():
    global running
    running = False
    return {"status": "Stopped"}

@app.get("/data")
def fetch_data():
    return get_records()
