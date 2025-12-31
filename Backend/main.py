import json
from fastapi import (
    FastAPI,
    WebSocket,
    WebSocketDisconnect,
    UploadFile,
    File
)
from fastapi.middleware.cors import CORSMiddleware

from rag.retrieve import retrieve_context
from llm.stream import stream_response
from llm.prompt import SYSTEM_PROMPT
from audio.speech_text import transcribe_audio
from audio.text_speech import text_to_speech



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # local dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/stt")
async def speech_to_text(file: UploadFile = File(...)):
    """
    Receives audio from frontend mic,
    converts it to text using Whisper,
    returns plain text.
    """
    audio_bytes = await file.read()
    text = transcribe_audio(audio_bytes)
    return {"text": text}



@app.websocket("/chat")
async def chat(ws: WebSocket):
    """
    WebSocket endpoint:
    - accepts text input
    - retrieves RAG context
    - streams text tokens
    - sends final voice response
    """

    await ws.accept()
    print("🔌 WebSocket connected")

    try:
        while True:
          
            raw = await ws.receive_text()

        
            if raw == "__interrupt__":
                await ws.send_json({"type": "interrupted"})
                continue

           
            try:
                payload = json.loads(raw)
                user_text = payload.get("text", "").strip()
            except json.JSONDecodeError:
                user_text = raw.strip()

            if not user_text:
                continue

            print(f"👤 User: {user_text}")

        
            context_docs = retrieve_context(user_text)

            if not context_docs:
                await ws.send_json({
                    "type": "assistant",
                    "value": "I don’t have enough personal context to answer that."
                })
                continue

       
            full_answer = ""

            for token in stream_response(
                SYSTEM_PROMPT,
                context_docs,
                user_text
            ):
                full_answer += token
                await ws.send_json({
                    "type": "token",
                    "value": token
                })

           
            await ws.send_json({"type": "done"})

            
            try:
                audio_bytes = text_to_speech(full_answer)
                await ws.send_bytes(audio_bytes)
            except Exception as tts_error:
                print("🔊 TTS error:", repr(tts_error))

    except WebSocketDisconnect:
        print("❌ WebSocket disconnected")

    except Exception as e:
        print("🔥 WebSocket error:", repr(e))

    finally:
        print("🔒 WebSocket closed")
