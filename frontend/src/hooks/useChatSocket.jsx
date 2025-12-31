
import React, { useEffect, useRef, useState } from "react";
import { Mic, Send, Volume2 } from "lucide-react";

// Custom Hook - useChatSocket
export default function useChatSocket() {
  const socketRef = useRef(null);
  const assistantBufferRef = useRef("");

  const [messages, setMessages] = useState([]);
  const [streamingText, setStreamingText] = useState("");
  const [assistantSpeaking, setAssistantSpeaking] = useState(false);
  const [audioQueue, setAudioQueue] = useState([]);

  useEffect(() => {
    const socket = new WebSocket("ws://127.0.0.1:8000/chat");
    socket.binaryType = "blob";
    socketRef.current = socket;

    socket.onopen = () => {
      console.log("✅ WebSocket connected");
    };

    socket.onmessage = (event) => {
      if (event.data instanceof Blob) {
        const audioBlob = new Blob([event.data], { type: "audio/wav" });
        const audioUrl = URL.createObjectURL(audioBlob);

        const audio = new Audio(audioUrl);
        audio.play().catch((err) => {
          console.error("Audio playback failed:", err);
        });

        return;
      }
      const msg = JSON.parse(event.data);

      if (msg.type === "token") {
        assistantBufferRef.current += msg.value;
        setStreamingText(assistantBufferRef.current);
        setAssistantSpeaking(true);
      }

      if (msg.type === "done") {
        const finalText = assistantBufferRef.current;

        if (finalText.trim()) {
          setMessages((prev) => [
            ...prev,
            { role: "assistant", text: finalText },
          ]);
        }

        assistantBufferRef.current = "";
        setStreamingText("");
        setAssistantSpeaking(false);
      }

      if (msg.type === "interrupted") {
        assistantBufferRef.current = "";
        setStreamingText("");
        setAssistantSpeaking(false);
      }
    };

    socket.onerror = (err) => {
      console.error("❌ WebSocket error", err);
    };

    socket.onclose = () => {
      console.warn("⚠️ WebSocket closed");
    };

    return () => socket.close();
  }, []);

  const sendText = (text) => {
    if (!socketRef.current || socketRef.current.readyState !== WebSocket.OPEN) {
      console.warn("WebSocket not ready");
      return;
    }

    socketRef.current.send(JSON.stringify({ text }));
    setMessages((prev) => [...prev, { role: "user", text }]);
  };

  const interrupt = () => {
    if (socketRef.current?.readyState === WebSocket.OPEN) {
      socketRef.current.send("__interrupt__");
    }

    assistantBufferRef.current = "";
    setStreamingText("");
    setAssistantSpeaking(false);
    setAudioQueue([]);
  };

  return {
    messages,
    streamingText,
    assistantSpeaking,
    sendText,
    interrupt,
    audioQueue,
  };
}