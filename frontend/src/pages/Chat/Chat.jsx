import "./Chat.css";
import { useState } from "react";
import { Send, Bot, User, Plus } from "lucide-react";
import { sendChatMessage } from "../../services/chatService";


function Chat() {
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const [messages, setMessages] = useState([
    {
      sender: "ai",
      text: "Hi! I am your AI Learning Assistant. Ask me anything."
    }
  ]);

  const chats = [
    "React Hooks",
    "FastAPI JWT",
    "Machine Learning",
    "Prompt Engineering"
  ];

  //  SEND MESSAGE TO BACKEND
 const sendMessage = async () => {
  if (!message.trim()) return;

  const currentQuestion = message;

  const userMsg = {
    sender: "user",
    text: currentQuestion,
  };

  setMessages((prev) => [...prev, userMsg]);
  setMessage("");
  setLoading(true);

  try {
    const aiResponse = await sendChatMessage(currentQuestion);

    setMessages((prev) => [
      ...prev,
      {
        sender: "ai",
        text: aiResponse,
      },
    ]);
  } catch (error) {
    console.error(error);
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
            <div key={index} className="history-item">
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
            <div key={index} className={`message ${msg.sender}`}>
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
            placeholder="Ask anything..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") sendMessage();
            }}
          />

          <button onClick={sendMessage}>
            <Send size={18} />
          </button>
        </div>

      </div>
    </div>
  );
}

export default Chat;