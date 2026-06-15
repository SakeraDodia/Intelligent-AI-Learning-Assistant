import "./PDFChat.css";

import {
  Upload,
  FileText,
  Send,
  Paperclip,
  Bot,
  FileSearch
} from "lucide-react";

function PDFChat() {

  const documents = [
    {
      name: "Attention_in_AI_Vs_NN.pdf",
      size: "8.4 MB"
    },
    {
      name: "LLM_Paper_2024.pdf",
      size: "5.2 MB"
    },
    {
      name: "RAG_Techniques.pdf",
      size: "3.8 MB"
    },
    {
      name: "Vector_Database.pdf",
      size: "2.1 MB"
    }
  ];

  return (
    <div className="pdf-chat-page">

      <div className="pdf-header">

        <h2>PDF Chat</h2>

        <button className="upload-btn">
          <Upload size={18} />
          Upload PDF
        </button>

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

            <div className="user-question">
              What is the main idea of this paper?
            </div>

            <div className="ai-answer">

              <div className="answer-header">

                <Bot size={18} />

                <span>AI Assistant</span>

              </div>

              <p>
                The paper introduces the Transformer
                model which relies solely on
                attention mechanisms.
              </p>

              <p>
                It removes recurrent networks and
                improves training efficiency while
                achieving state-of-the-art results.
              </p>

            </div>

          </div>

          <div className="pdf-input">

            <button className="attach-btn">

              <Paperclip size={18} />

            </button>

            <input
              type="text"
              placeholder="Ask a question about your PDF..."
            />

            <button className="send-btn">

              <Send size={18} />

            </button>

          </div>

        </div>

      </div>

    </div>
  );
}

export default PDFChat;