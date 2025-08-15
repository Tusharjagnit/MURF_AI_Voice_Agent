import os
import logging

try:
    import assemblyai as aai
except Exception:
    aai = None

logger = logging.getLogger(__name__)


def transcribe_audio(audio_bytes: bytes) -> str:
    """Transcribe raw audio bytes using AssemblyAI.

    Raises RuntimeError on missing config or transcription failure.
    """
    if not aai:
        raise RuntimeError("AssemblyAI SDK not installed")

    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise RuntimeError("ASSEMBLYAI_API_KEY not set")

    aai.settings.api_key = api_key
    transcriber = aai.Transcriber()

    try:
        transcript = transcriber.transcribe(audio_bytes)
        if not transcript or not getattr(transcript, 'text', None):
            raise RuntimeError("Empty transcription result")
        return transcript.text.strip()
    except Exception as e:
        logger.exception("STT transcription failed")
        raise RuntimeError(f"STT transcription failed: {e}")
