import "./Notes.css";

import {
  Search,
  Plus,
  FileText,
  Download
} from "lucide-react";

function Notes() {

  const notes = [
    "React Fundamentals",
    "FastAPI Authentication",
    "Machine Learning Basics",
    "Prompt Engineering"
  ];

  return (
    <div className="notes-page">

      <div className="notes-header">

        <h2>AI Notes Generator</h2>

        <button className="create-btn">
          <Plus size={18} />
          Create Notes
        </button>

      </div>

      <div className="search-box">

        <Search size={18} />

        <input
          type="text"
          placeholder="Search notes..."
        />

      </div>

      <div className="notes-grid">

        {notes.map((note, index) => (

          <div
            key={index}
            className="note-card"
          >

            <FileText size={30} />

            <h3>{note}</h3>

            <p>
              AI generated study notes
            </p>

            <button>
              <Download size={16} />
              Download
            </button>

          </div>

        ))}

      </div>

    </div>
  );
}

export default Notes;