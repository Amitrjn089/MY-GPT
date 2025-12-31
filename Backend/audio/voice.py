# backend/audio/vad.py
import numpy as np
import time

class VoiceActivityDetector:
    def __init__(
        self,
        rms_threshold: float = 0.02,
        silence_duration: float = 1.0
    ):
        """
        rms_threshold: minimum energy to consider as speech
        silence_duration: seconds of silence to mark speech end
        """
        self.rms_threshold = rms_threshold
        self.silence_duration = silence_duration
        self.last_voice_time = None
        self.speaking = False

    def rms(self, audio_chunk: bytes) -> float:
        """Compute RMS energy of PCM16 audio"""
        samples = np.frombuffer(audio_chunk, dtype=np.int16)
        if len(samples) == 0:
            return 0.0
        return np.sqrt(np.mean(samples.astype(np.float32) ** 2)) / 32768.0

    def process(self, audio_chunk: bytes) -> str:
        """
        Returns:
        - "speech_start"
        - "speech_continue"
        - "speech_end"
        - "silence"
        """
        energy = self.rms(audio_chunk)
        current_time = time.time()

        if energy > self.rms_threshold:
            self.last_voice_time = current_time
            if not self.speaking:
                self.speaking = True
                return "speech_start"
            return "speech_continue"

        if self.speaking:
            if current_time - self.last_voice_time > self.silence_duration:
                self.speaking = False
                return "speech_end"

        return "silence"
