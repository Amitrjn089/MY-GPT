import "./App.css";
import useChatSocket from "./hooks/useChatSocket";
import ChatBox from "./components/ChatBox";
import MicController from "./components/MicController";
import AudioPlayer from "./components/AudioPlayer";
import { Send, Volume2 } from "lucide-react";
import { useState } from "react";

function App() {
  const {
    messages,
    streamingText,
    assistantSpeaking,
    sendText,
    interrupt,
  } = useChatSocket();

  const [inputValue, setInputValue] = useState("");

  const handleSend = () => {
    if (inputValue.trim()) {
      sendText(inputValue);
      setInputValue("");
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex w-full flex-col h-screen bg-white">
      <div className="border-b border-gray-200 px-6 py-4">
        <h1 className="text-xl text-center font-semibold text-gray-900">
          Personal Assistant
        </h1>
        {assistantSpeaking && (
          <div className="flex items-center gap-2 mt-1 text-sm text-blue-600">
            <Volume2 className="w-4 h-4 animate-pulse" />
            <span>Speaking...</span>
          </div>
        )}
      </div>

      {/* Chat Area */}
      <ChatBox messages={messages} streamingText={streamingText} />

      {/* Input Area */}
      <div className="border-t border-gray-200 px-4 py-4">
        <div className="flex items-end gap-3 max-w-4xl mx-auto">
          <MicController interrupt={interrupt} onText={sendText} />
          
          <div className="flex-1 relative">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Type your message..."
              className="w-full px-4 py-3 pr-12 rounded-full border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900 placeholder-gray-400"
            />
            <button
              onClick={handleSend}
              disabled={!inputValue.trim()}
              className="absolute right-2 top-1/2 -translate-y-1/2 p-2 rounded-full bg-blue-600 text-white hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
            >
              <Send className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;