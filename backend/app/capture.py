import subprocess
from config import STREAM_URL, AUDIO_FILE, CHUNK_DURATION

def capture_audio():
    cmd = [
        "ffmpeg",
        "-y",
        "-i", STREAM_URL,
        "-t", str(CHUNK_DURATION),
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        AUDIO_FILE
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
