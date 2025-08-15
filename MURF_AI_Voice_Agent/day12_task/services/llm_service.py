import os
import logging

try:
    import google.generativeai as genai
except Exception:
    genai = None

logger = logging.getLogger(__name__)


def generate_response(history: list, user_text: str) -> str:
    """Generate LLM response using Google Gemini.

    history should be a list of dicts matching the Gemini chat format.
    """
    if not genai:
        raise RuntimeError("Google Generative AI SDK not installed")

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set")

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        chat_session = model.start_chat(history=history or [])
        llm_response = chat_session.send_message(user_text)
        text = (llm_response.text or "").strip()
        if not text:
            raise RuntimeError("LLM returned empty response")
        return text
    except Exception as e:
        logger.exception("LLM generation failed")
        raise RuntimeError(f"LLM generation failed: {e}")
