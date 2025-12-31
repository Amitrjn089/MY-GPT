import { useEffect, useRef } from "react";

export default function ChatBox({ messages, streamingText }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, streamingText]);

  return (
    <div className="flex-1 w-full  overflow-y-auto px-4 py-6 space-y-4">
      {messages.length === 0 && !streamingText && (
        <div className="flex items-center justify-center h-full text-gray-400">
          <p className="text-center">
            Start a conversation with your AI assistant
          </p>
        </div>
      )}
      
      {messages.map((msg, index) => (
        <div
          key={index}
          className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
        >
          <div
            className={`max-w-[80%] rounded-2xl px-4 py-3 ${
              msg.role === "user"
                ? "bg-blue-600 text-white"
                : "bg-gray-100 text-gray-900"
            }`}
          >
            <div className="text-sm font-medium mb-1 opacity-70">
              {msg.role === "user" ? "You" : "Assistant"}
            </div>
            <div className="text-[15px] leading-relaxed">{msg.text}</div>
          </div>
        </div>
      ))}
      
      {streamingText && (
        <div className="flex justify-start">
          <div className="max-w-[80%] rounded-2xl px-4 py-3 bg-gray-100 text-gray-900">
            <div className="text-sm font-medium mb-1 opacity-70">Assistant</div>
            <div className="text-[15px] leading-relaxed">
              {streamingText}
              <span className="inline-block w-0.5 h-5 bg-gray-900 ml-1 animate-pulse"></span>
            </div>
          </div>
        </div>
      )}

      <div ref={bottomRef} />
    </div>
  );
}