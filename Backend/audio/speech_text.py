from faster_whisper import WhisperModel
import tempfile

# Load once (important)
model = WhisperModel(
    "base",
    compute_type="int8"
)

def transcribe_audio(audio_bytes: bytes) -> str:
    """
    Converts raw audio bytes into text using Whisper
    """
    with tempfile.NamedTemporaryFile(suffix=".wav") as f:
        f.write(audio_bytes)
        f.flush()

        segments, _ = model.transcribe(f.name)
        text = " ".join(segment.text for segment in segments)

    return text.strip()
