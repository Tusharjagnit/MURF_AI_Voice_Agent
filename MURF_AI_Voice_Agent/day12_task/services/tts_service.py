import os
import logging
import httpx

logger = logging.getLogger(__name__)


async def synthesize_text_to_speech(text: str, voice_id: str = "en-US-charles") -> str:
    """Call Murf API to synthesize TTS and return the audio URL.

    Raises RuntimeError on failure.
    """
    api_key = os.getenv("MURF_API_KEY")
    if not api_key:
        raise RuntimeError("MURF_API_KEY not set")

    murf_url = "https://api.murf.ai/v1/speech/generate"
    headers = {"api-key": api_key, "Content-Type": "application/json"}
    payload = {"text": text, "voiceId": voice_id, "format": "mp3"}

    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(120.0, connect=10.0)) as client:
            resp = await client.post(murf_url, json=payload, headers=headers)
            if resp.status_code != 200:
                raise RuntimeError(f"Murf API error {resp.status_code}: {resp.text[:200]}")
            data = resp.json()
            audio_url = data.get("audioFile")
            if not audio_url:
                raise RuntimeError("Murf response missing audioFile")
            return audio_url
    except Exception as e:
        logger.exception("TTS failed")
        raise RuntimeError(f"TTS failed: {e}")
