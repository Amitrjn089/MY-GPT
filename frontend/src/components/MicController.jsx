import { useRef } from "react";
import { useState } from "react";
import { Mic } from "lucide-react";


export default function MicController({ interrupt, onText }) {
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);
  const stopTimeoutRef = useRef(null);
  const [isRecording, setIsRecording] = useState(false);

  const startRecording = async () => {
    interrupt();
    setIsRecording(true);

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const recorder = new MediaRecorder(stream);
    mediaRecorderRef.current = recorder;
    chunksRef.current = [];

    recorder.ondataavailable = (e) => {
      chunksRef.current.push(e.data);
    };

    recorder.onstop = async () => {
      setIsRecording(false);
      const audioBlob = new Blob(chunksRef.current, { type: "audio/wav" });
      const formData = new FormData();
      formData.append("file", audioBlob);

      const res = await fetch("http://127.0.0.1:8000/stt", {
        method: "POST",
        body: formData
      });

      const data = await res.json();
      if (data.text && data.text.trim()) {
        onText(data.text);
      }
    };

    recorder.start();
  };

  const stopRecording = () => {
    stopTimeoutRef.current = setTimeout(() => {
      mediaRecorderRef.current?.stop();
    }, 400);
  };

  return (
    <button
      onMouseDown={startRecording}
      onMouseUp={stopRecording}
      onMouseLeave={stopRecording}
      className={`p-3 rounded-full transition-all duration-200 ${
        isRecording
          ? "bg-red-500 text-white scale-110"
          : "bg-gray-100 text-gray-700 hover:bg-gray-200"
      }`}
    >
      <Mic className="w-5 h-5" />
    </button>
  );
}