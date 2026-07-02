import "./Chat.css";
import { useState } from "react";
import { Send, Bot, User, Plus } from "lucide-react";

function Chat() {
  const [message, setMessage] = useState("");

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

  const handleSend = () => {
    if (!message.trim()) return;

    const userMessage = {
      sender: "user",
      text: message
    };

    const aiMessage = {
      sender: "ai",
      text: "This is a static UI. AI response will appear here after backend integration."
    };

    setMessages((prev) => [
      ...prev,
      userMessage,
      aiMessage
    ]);

    setMessage("");
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

        </div>

        {/* Input */}

        <div className="chat-input-area">

          <input
            type="text"
            placeholder="Ask anything..."
            value={message}
            onChange={(e) =>
              setMessage(e.target.value)
            }
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                handleSend();
              }
            }}
          />

          <button onClick={handleSend}>
            <Send size={18} />
          </button>

        </div>

      </div>

    </div>
  );
}

export default Chat;