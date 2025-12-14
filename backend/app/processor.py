import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phi"

def summarize(text: str) -> str:
    """
    Generate a short summary (<= 15 words) for a 1-minute TV news transcript
    using a local LLM via Ollama.
    """

    if not text or len(text.strip()) == 0:
        return "No meaningful speech detected"

    prompt = (
        "Summarize the following TV news transcript in 15 words or fewer.\n\n"
        f"{text}\n\n"
        "Summary:"
    )

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=90
        )
        response.raise_for_status()

        summary = response.json().get("response", "").strip()

        # Hard safety limit
        return " ".join(summary.split()[:15])

    except Exception as e:
        # Fallback so the pipeline never breaks
        return "Summary generation failed"
