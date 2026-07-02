import "./PDFChat.css";
import { useState } from "react";

import {
  Upload,
  FileText,
  Send,
  Paperclip,
  Bot,
  FileSearch,
  User
} from "lucide-react";

import {
  uploadPDF,
  askPDF
} from "../../services/pdfService";

function PDFChat() {

  const [documents, setDocuments] = useState([]);

  const [question, setQuestion] = useState("");

  const [messages, setMessages] = useState([
    {
      sender: "user",
      text: "What is the main idea of this paper?"
    },
    {
      sender: "ai",
      text: "The paper introduces the Transformer model which relies solely on attention mechanisms."
    }
  ]);

  const handleUpload = async (e) => {

    const file = e.target.files[0];

    if (!file) return;

    try {

      await uploadPDF(file);

      setDocuments(prev => [
        {
          name: file.name,
          size: `${(file.size / 1024 / 1024).toFixed(1)} MB`
        },
        ...prev
      ]);

    } catch (error) {

      console.error(error);

      alert("Upload Failed");
    }
  };

  const handleSend = async () => {

    if (!question.trim()) return;

    const currentQuestion = question;

    setMessages(prev => [
      ...prev,
      {
        sender: "user",
        text: currentQuestion
      }
    ]);

    setQuestion("");

    try {

      const response = await askPDF(currentQuestion);

      setMessages(prev => [
        ...prev,
        {
          sender: "ai",
          text: response.data.answer
        }
      ]);

    } catch (error) {

      console.error(error);

      setMessages(prev => [
        ...prev,
        {
          sender: "ai",
          text: "Unable to generate answer."
        }
      ]);
    }
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
            onChange={handleUpload}
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

                <FileText size={20} />

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
                  Ask questions about the selected document
                </p>

              </div>

            </div>

          </div>

          <div className="pdf-messages">

            {messages.map((msg, index) => (

              msg.sender === "user" ? (

                <div
                  key={index}
                  className="user-question"
                >

                  <User size={16} />

                  {msg.text}

                </div>

              ) : (

                <div
                  key={index}
                  className="ai-answer"
                >

                  <div className="answer-header">

                    <Bot size={18} />

                    <span>
                      AI Assistant
                    </span>

                  </div>

                  <p>{msg.text}</p>

                </div>

              )

            ))}

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