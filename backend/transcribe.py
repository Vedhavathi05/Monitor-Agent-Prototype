import whisper
from config import AUDIO_FILE

model = whisper.load_model("base")

def transcribe_audio():
    result = model.transcribe(AUDIO_FILE)
    return result["text"]
