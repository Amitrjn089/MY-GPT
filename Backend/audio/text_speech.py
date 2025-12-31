import pyttsx3
import tempfile
import subprocess

engine = pyttsx3.init()
engine.setProperty("rate", 165)

def text_to_speech(text: str) -> bytes:
    with tempfile.NamedTemporaryFile(suffix=".aiff", delete=False) as aiff:
        aiff_path = aiff.name

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as wav:
        wav_path = wav.name

    engine.save_to_file(text, aiff_path)
    engine.runAndWait()
    subprocess.run([
        "afconvert",
        aiff_path,
        wav_path,
        "-f", "WAVE",
        "-d", "LEI16"
    ], check=True)

    with open(wav_path, "rb") as f:
        return f.read()
