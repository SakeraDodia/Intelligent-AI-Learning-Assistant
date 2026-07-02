import "./PDFChat.css";
import { useState } from "react";

import {
  Upload,
  FileText,
  Send,
  Paperclip,
  Bot,
  FileSearch,
  User,
} from "lucide-react";

function PDFChat() {
  const documents = [
    {
      name: "Machine Learning Notes.pdf",
      size: "4.2 MB",
    },
    {
      name: "Deep Learning Guide.pdf",
      size: "8.1 MB",
    },
    {
      name: "Python Handbook.pdf",
      size: "2.8 MB",
    },
    {
      name: "NLP Basics.pdf",
      size: "6.5 MB",
    },
  ];

  const sampleMessages = [
    {
      sender: "user",
      text: "What is Machine Learning?",
    },
    {
      sender: "ai",
      text: "Machine Learning is a branch of Artificial Intelligence that enables computers to learn patterns from data and make predictions without being explicitly programmed.",
    },
    {
      sender: "user",
      text: "Explain Supervised Learning.",
    },
    {
      sender: "ai",
      text: "Supervised Learning is a machine learning technique where the model learns using labelled data. It predicts outputs based on examples provided during training.",
    },
    {
      sender: "user",
      text: "Give some examples.",
    },
    {
      sender: "ai",
      text: "Examples include Linear Regression, Logistic Regression, Decision Trees, Random Forest, Support Vector Machine (SVM), and Neural Networks.",
    },
  ];

  const [question, setQuestion] = useState("");

  const handleSend = () => {
    if (!question.trim()) return;

    alert(
      "This is a static UI.\n\nBackend integration will be added later."
    );

    setQuestion("");
  };

  return (
    <div className="pdf-chat-page">
      <div className="pdf-header">
        <h2>PDF Chat</h2>

        <label className="upload-btn">
          <Upload size={18} />

          Upload PDF

          <input
            type="file"
            accept=".pdf"
            hidden
          />
        </label>
      </div>

      <div className="pdf-content">
        {/* Left Panel */}

        <div className="documents-panel">
          <h3>My Documents</h3>

          <div className="documents-list">
            {documents.map((doc, index) => (
              <div
                key={index}
                className={
                  index === 0
                    ? "document-card active"
                    : "document-card"
                }
              >
                <FileText size={22} />

                <div>
                  <h4>{doc.name}</h4>

                  <p>{doc.size}</p>
                </div>
              </div>
            ))}
          </div>

          <button className="folder-btn">
            + Add New Folder
          </button>
        </div>

        {/* Right Panel */}

        <div className="pdf-chat-area">
          <div className="pdf-chat-topbar">
            <div className="topbar-left">
              <div className="pdf-chat-icon">
                <FileSearch size={24} />
              </div>

              <div>
                <h2>Chat with your PDF</h2>

                <p>
                  Ask questions about the selected
                  document
                </p>
              </div>
            </div>
          </div>

          <div className="pdf-messages">
            {sampleMessages.map((msg, index) =>
              msg.sender === "user" ? (
                <div
                  key={index}
                  className="user-question"
                >
                  <User size={18} />

                  <span>{msg.text}</span>
                </div>
              ) : (
                <div
                  key={index}
                  className="ai-answer"
                >
                  <div className="answer-header">
                    <Bot size={18} />

                    <span>AI Assistant</span>
                  </div>

                  <p>{msg.text}</p>
                </div>
              )
            )}
          </div>

          <div className="pdf-input">
            <button className="attach-btn">
              <Paperclip size={18} />
            </button>

            <input
              type="text"
              value={question}
              onChange={(e) =>
                setQuestion(e.target.value)
              }
              placeholder="Ask a question about your PDF..."
            />

            <button
              className="send-btn"
              onClick={handleSend}
            >
              <Send size={18} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default PDFChat;