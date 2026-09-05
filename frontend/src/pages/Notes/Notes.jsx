import "./Notes.css";

import { useState } from "react";

import {
  Search,
  Plus,
  FileText,
  Download
} from "lucide-react";

import { generateNotes } from "../../services/api";

function Notes() {

  const [notes, setNotes] = useState([]);

  const [topic, setTopic] = useState("");

  const [level, setLevel] = useState("beginner");

  const [loading, setLoading] = useState(false);

  const [search, setSearch] = useState("");

  const [showCreate, setShowCreate] = useState(false);


  // ======================================================
  // GENERATE NOTES
  // ======================================================

  const handleGenerateNotes = async () => {

    if (!topic.trim() || loading) {
      return;
    }

    setLoading(true);

    try {

      const data = await generateNotes(
        topic,
        level
      );

      const newNote = {
        id: Date.now(),
        title: topic,
        content:
          data.notes ||
          data.response ||
          data.content ||
          "No notes generated."
      };

      setNotes((prev) => [
        newNote,
        ...prev
      ]);

      setTopic("");

      setShowCreate(false);

    } catch (error) {

      console.error(
        "Notes API Error:",
        error
      );

      alert(
        "Unable to generate notes. Please check the backend."
      );

    } finally {

      setLoading(false);

    }
  };


  // ======================================================
  // DOWNLOAD NOTES
  // ======================================================

  const handleDownload = (note) => {

    const blob = new Blob(
      [note.content],
      {
        type: "text/plain"
      }
    );

    const url =
      URL.createObjectURL(blob);

    const a =
      document.createElement("a");

    a.href = url;

    a.download =
      `${note.title}.txt`;

    a.click();

    URL.revokeObjectURL(url);
  };


  // ======================================================
  // SEARCH
  // ======================================================

  const filteredNotes =
    notes.filter((note) =>
      note.title
        .toLowerCase()
        .includes(search.toLowerCase())
    );


  return (
    <div className="notes-page">

      <div className="notes-header">

        <h2>
          AI Notes Generator
        </h2>

        <button
          className="create-btn"
          onClick={() =>
            setShowCreate((prev) => !prev)
          }
        >

          <Plus size={18} />

          Create Notes

        </button>

      </div>


      {/* CREATE NOTES */}

      {showCreate && (

        <div className="search-box">

          <input
            type="text"
            placeholder="Enter topic..."
            value={topic}
            onChange={(e) =>
              setTopic(e.target.value)
            }
          />

          <select
            value={level}
            onChange={(e) =>
              setLevel(e.target.value)
            }
          >

            <option value="beginner">
              Beginner
            </option>

            <option value="intermediate">
              Intermediate
            </option>

            <option value="advanced">
              Advanced
            </option>

          </select>

          <button
            onClick={handleGenerateNotes}
            disabled={
              loading ||
              !topic.trim()
            }
          >

            {loading
              ? "Generating..."
              : "Generate"}

          </button>

        </div>

      )}


      {/* SEARCH */}

      <div className="search-box">

        <Search size={18} />

        <input
          type="text"
          placeholder="Search notes..."
          value={search}
          onChange={(e) =>
            setSearch(e.target.value)
          }
        />

      </div>


      {/* NOTES */}

      <div className="notes-grid">

        {filteredNotes.length === 0 && (

          <p>
            No notes available. Create your first AI note.
          </p>

        )}

        {filteredNotes.map(
          (note) => (

            <div
              key={note.id}
              className="note-card"
            >

              <FileText size={30} />

              <h3>
                {note.title}
              </h3>

              <p>
                {note.content}
              </p>

              <button
                onClick={() =>
                  handleDownload(note)
                }
              >

                <Download size={16} />

                Download

              </button>

            </div>

          )
        )}

      </div>

    </div>
  );
}

export default Notes;