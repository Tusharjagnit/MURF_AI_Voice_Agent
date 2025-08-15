# Day 12: Revamped UI - Backend Cleanup
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os
import logging
from typing import Dict, List, Optional

from pydantic import BaseModel

# services
from services import stt_service, llm_service, tts_service

# Load env from the current script's directory
script_dir = os.path.dirname(os.path.realpath(__file__))
dotenv_path = os.path.join(script_dir, '.env')
load_dotenv(dotenv_path=dotenv_path)

logger = logging.getLogger("day12")
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Day 12 - Revamped Voice Agent")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# --- Pydantic models for clarity ---
class ChatResponse(BaseModel):
    success: bool
    audio_url: Optional[str] = None
    transcript: Optional[str] = None
    llm_text: Optional[str] = None


# --- Standardized error response helper ---
def error_response(status_code: int, error_code: str, message: str, details: Optional[str] = None):
    fallback_audio_map = {
        "STT": "stt_error.mp3",
        "LLM": "llm_error.mp3",
        "TTS": "tts_error.mp3",
        "CONNECTION": "connection_error.mp3"
    }
    fallback_file = fallback_audio_map.get(error_code, "connection_error.mp3")
    
    logger.error("%s: %s (%s)", error_code, message, details)
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "error": message,
            "details": details,
            "fallback_audio_path": f"/static/fallback_audio/{fallback_file}"
        }
    )


# Simple in-memory chat history store (session_id -> history)
ChatHistory = List[Dict[str, any]] 
chats: Dict[str, ChatHistory] = {}


def append_message(session_id: str, role: str, content: str) -> None:
    api_role = "model" if role == "assistant" else "user"
    history = chats.setdefault(session_id, [])
    history.append({"role": api_role, "parts": [content]})


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/agent/chat/{session_id}", response_model=ChatResponse)
async def agent_chat(session_id: str, file: UploadFile = File(...)):
    try:
        # Read audio bytes
        audio_bytes = await file.read()

        # 1) STT
        try:
            user_text = stt_service.transcribe_audio(audio_bytes)
        except Exception as e:
            return error_response(502, "STT", "STT transcription failed", str(e))

        # 2) LLM
        try:
            llm_text = llm_service.generate_response(chats.get(session_id, []), user_text)
        except Exception as e:
            return error_response(502, "LLM", "LLM generation failed", str(e))

        # Append messages after successful LLM
        append_message(session_id, "user", user_text)
        append_message(session_id, "assistant", llm_text)

        # 3) TTS
        try:
            audio_url = await tts_service.synthesize_text_to_speech(llm_text)
        except Exception as e:
            return error_response(502, "TTS", "TTS synthesis failed", str(e))

        return {
            "success": True,
            "audio_url": audio_url,
            "transcript": user_text,
            "llm_text": llm_text,
        }
    except Exception as e:
        logger.exception("Unexpected error in agent_chat")
        return error_response(500, "CONNECTION", "Chat processing failed", str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
