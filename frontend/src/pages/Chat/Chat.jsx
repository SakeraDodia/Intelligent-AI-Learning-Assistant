import "./Chat.css";

import { useState } from "react";

import {
  Send,
  Bot,
  User,
  Plus
} from "lucide-react";

function Chat() {
  const [message, setMessage] = useState("");

  const chats = [
    "React Hooks",
    "FastAPI JWT",
    "Machine Learning",
    "Prompt Engineering"
  ];

  const messages = [
    {
      sender: "user",
      text: "Explain React Hooks."
    },
    {
      sender: "ai",
      text: "React Hooks allow you to use state and lifecycle features inside functional components."
    }
  ];

  return (
    <div className="chat-page">

      {/* Chat History */}

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

        <div className="messages-container">

          {messages.map((msg, index) => (
            <div
              key={index}
              className={`message ${msg.sender}`}
            >
              <div className="message-icon">
                {msg.sender === "user"
                  ? <User size={18} />
                  : <Bot size={18} />
                }
              </div>

              <div className="message-content">
                {msg.text}
              </div>

            </div>
          ))}

        </div>

        <div className="chat-input-area">

          <input
            type="text"
            placeholder="Ask anything..."
            value={message}
            onChange={(e) =>
              setMessage(e.target.value)
            }
          />

          <button>
            <Send size={18} />
          </button>

        </div>

      </div>

    </div>
  );
}

export default Chat;