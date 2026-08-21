import "./Chat.css";
import { useState } from "react";
import { Send, Bot, User, Plus } from "lucide-react";
import { sendChatMessage } from "../services/api";

function Chat() {
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const [messages, setMessages] = useState([
    {
      sender: "ai",
      text: "👋 Hi! I am your AI Learning Assistant. Ask me anything about AI, Machine Learning, Deep Learning, Python, React, or any technical topic."
    }
  ]);

  const chats = [
    "React Hooks",
    "FastAPI JWT",
    "Machine Learning",
    "Prompt Engineering",
    "Deep Learning",
    "Python Basics"
  ];

  const handleSend = async () => {
    if (!message.trim() || loading) return;

    const userMessage = message.trim();

    // Add user message immediately
    setMessages((prev) => [
      ...prev,
      {
        sender: "user",
        text: userMessage
      }
    ]);

    // Clear input
    setMessage("");

    // Start loading
    setLoading(true);

    try {
      // Send message to FastAPI
      const data = await sendChatMessage(userMessage);

      // Add AI response
      setMessages((prev) => [
        ...prev,
        {
          sender: "ai",
          text: data.response
        }
      ]);
    } catch (error) {
      console.error("Chat API Error:", error);

      setMessages((prev) => [
        ...prev,
        {
          sender: "ai",
          text: "❌ Unable to connect to the AI backend. Please make sure the FastAPI server is running."
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-page">

      {/* Sidebar */}

      <div className="chat-sidebar">

        <button className="new-chat-btn">
          <Plus size={18} />
          New Chat
        </button>

        <div className="chat-history">

          {chats.map((chat, index) => (
            <div
              key={index}
              className="history-item"
            >
              {chat}
            </div>
          ))}

        </div>

      </div>

      {/* Chat Area */}

      <div className="chat-container">

        <div className="chat-header">

          <div className="header-left">

            <Bot size={22} />

            <h2>AI Learning Assistant</h2>

          </div>

        </div>

        {/* Messages */}

        <div className="messages-container">

          {messages.map((msg, index) => (

            <div
              key={index}
              className={`message ${msg.sender}`}
            >

              <div className="message-icon">

                {msg.sender === "user" ? (
                  <User size={18} />
                ) : (
                  <Bot size={18} />
                )}

              </div>

              <div className="message-content">
                {msg.text}
              </div>

            </div>

          ))}

          {/* Loading message */}

          {loading && (
            <div className="message ai">

              <div className="message-icon">
                <Bot size={18} />
              </div>

              <div className="message-content">
                Thinking...
              </div>

            </div>
          )}

        </div>

        {/* Input */}

        <div className="chat-input-area">

          <input
            type="text"
            placeholder={
              loading
                ? "AI is generating a response..."
                : "Ask anything..."
            }
            value={message}
            disabled={loading}
            onChange={(e) =>
              setMessage(e.target.value)
            }
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                handleSend();
              }
            }}
          />

          <button
            onClick={handleSend}
            disabled={loading || !message.trim()}
          >
            <Send size={18} />
          </button>

        </div>

      </div>

    </div>
  );
}

export default Chat;