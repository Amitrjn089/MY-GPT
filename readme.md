# Personal Digital Assistant

A **full-stack, local, privacy-first personal digital assistant** with real-time streaming responses, voice & text interaction, interruption support, and strict personal-data-only boundaries.

All processing happens **locally** — no cloud APIs, no data leaves your machine.

## ✨ Features

- Real-time **token-by-token** streaming responses (text + voice)
- **Voice input** using browser microphone + faster-whisper
- **Voice output** with local TTS
- **Real-time interruption** (stop speaking/typing = instant stop)
- **Strict RAG boundary** — only answers using your personal data
- Gracefully refuses or asks for clarification when context is missing
- Clean, production-oriented architecture
- Fully explainable end-to-end implementation

## 🏗️ Architecture
  Frontend (React + Vite)
├─ Chat UI ── real-time streaming text
├─ Mic Controller ── push-to-talk
└─ Audio Player ── queue-based voice playback
↓ WebSocket + HTTP
Backend (FastAPI)
├─ WebSocket /chat
│    ├─ Token streaming
│    ├─ Interruption handling
│    └─ Voice synthesis trigger
├─ POST /stt ── faster-whisper (audio → text)
├─ RAG Pipeline
│    ├─ all-MiniLM-L6-v2 embeddings
│    └─ FAISS flat index
└─ TTS ── local text-to-speech (piper / Coqui / etc.)


## 🛠️ Tech Stack

| Layer              | Technology                          | Purpose                              |
|--------------------|-------------------------------------|--------------------------------------|
| Frontend           | React + Vite + TypeScript           | Modern, fast UI                      |
| Backend            | FastAPI + WebSockets                | Async API & real-time streaming      |
| Speech-to-Text     | faster-whisper                      | Fast, accurate, local STT            |
| Embeddings         | sentence-transformers (all-MiniLM)  | Lightweight & good quality           |
| Vector Store       | FAISS                               | Very fast similarity search          |
| Text-to-Speech     | piper / Coqui TTS / MeloTTS         | Natural local voice synthesis        |
| Styling            | Tailwind CSS / shadcn/ui            | Clean, modern look                   |

## 🚀 Quick Start

### Backend

```bash
cd backend
# Recommended: use uv or poetry
uv venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt

# (Optional) Download models first time
python -c "from faster_whisper import WhisperModel; WhisperModel('medium')"

# Run
uvicorn main:app --host 0.0.0.0 --port 8000
# or with auto-reload (dev)
uvicorn main:app --reload

cd frontend

npm install
# or
pnpm install
# or
bun install

npm run dev
# or
pnpm dev
# or
bun dev

PI/
├── backend/
│   ├── main.py
│   ├── api/
│   │   ├── chat.py
│   │   ├── stt.py
│   │   └── rag.py
│   ├── core/
│   │   ├── config.py
│   │   ├── models.py
│   │   └── tts.py
│   ├── rag/
│   │   ├── embeddings.py
│   │   ├── index.py
│   │   └── retriever.py
│   ├── data/
│   │   └── documents/          ← Put your personal files here (txt, md, pdf...)
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Chat.tsx
│   │   │   ├── Message.tsx
│   │   │   ├── VoiceButton.tsx
│   │   │   └── AudioPlayer.tsx
│   │   ├── hooks/
│   │   │   └── useWebSocket.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── public/
│   └── package.json
│
├── README.md
└── .gitignore
