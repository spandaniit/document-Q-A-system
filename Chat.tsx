import React, { useState } from "react";
import axios from "axios";

interface Message {
  role: "user" | "assistant";
  text: string;
}

const Chat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [query, setQuery] = useState("");

  const sendMessage = async () => {
    if (!query.trim()) return;

    const userMessage = { role: "user" as const, text: query };
    setMessages((prev) => [...prev, userMessage]);

    const response = await axios.post("/api/ask", new URLSearchParams({ query }));
    const answer = response.data.answer;

    const assistantMessage = { role: "assistant" as const, text: answer };
    setMessages((prev) => [...prev, assistantMessage]);

    setQuery("");
  };

  return (
    <div className="w-full max-w-2xl flex flex-col gap-4">
      <div className="bg-white shadow rounded-lg p-4 h-96 overflow-y-auto">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`mb-2 ${
              msg.role === "user" ? "text-right" : "text-left"
            }`}
          >
            <span
              className={`inline-block px-3 py-2 rounded-lg ${
                msg.role === "user"
                  ? "bg-blue-500 text-white"
                  : "bg-gray-200 text-black"
              }`}
            >
              {msg.text}
            </span>
          </div>
        ))}
      </div>

      <div className="flex gap-2">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="flex-1 border px-3 py-2 rounded-lg"
          placeholder="Ask a question..."
        />
        <button
          onClick={sendMessage}
          className="bg-green-500 text-white px-4 py-2 rounded-lg"
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default Chat;