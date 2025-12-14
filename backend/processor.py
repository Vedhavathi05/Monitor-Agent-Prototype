import requests
import re
from collections import Counter

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phi:latest"
MAX_INPUT_CHARS = 1200

STOPWORDS = {
    "the", "is", "are", "was", "were", "and", "or", "to", "of", "in", "on",
    "for", "with", "as", "by", "at", "from", "that", "this", "it", "be",
    "has", "have", "had", "will", "would", "can", "could", "should"
}

def extractive_fallback(text: str) -> str:
    """Deterministic fallback summary (always works)"""
    sentences = re.split(r"(?<=[.!?])\s+", text)
    words = re.findall(r"\b[a-zA-Z]+\b", text.lower())
    keywords = [w for w in words if w not in STOPWORDS]
    freq = Counter(keywords)

    scored = []
    for s in sentences:
        score = sum(freq.get(w.lower(), 0) for w in re.findall(r"\b[a-zA-Z]+\b", s))
        scored.append((score, s))

    if not scored:
        return "No meaningful speech detected"

    best = max(scored, key=lambda x: x[0])[1]
    return " ".join(best.split()[:15])

def summarize(text: str) -> str:
    if not text or len(text.strip()) < 30:
        return "No meaningful speech detected"

    trimmed_text = text.strip()[:MAX_INPUT_CHARS]

    prompt = (
        "Summarize the following TV news transcript in 15 words or fewer.\n\n"
        f"{trimmed_text}\n\nSummary:"
    )

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )
        response.raise_for_status()

        summary = response.json().get("response", "").strip()
        return " ".join(summary.split()[:15])

    except Exception as e:
        print("OLLAMA FAILED — USING FALLBACK:", e)
        return extractive_fallback(text)

