import "./History.css";

import {
  Search,
  MessageSquare,
  Brain,
  FileText,
  Mic
} from "lucide-react";

function History() {

  const history = [
    {
      title: "React Hooks Discussion",
      type: "Chat",
      icon: <MessageSquare size={20} />,
      date: "Today"
    },
    {
      title: "Machine Learning Quiz",
      type: "Quiz",
      icon: <Brain size={20} />,
      date: "Yesterday"
    },
    {
      title: "Frontend Interview",
      type: "Interview",
      icon: <Mic size={20} />,
      date: "2 Days Ago"
    },
    {
      title: "React Documentation.pdf",
      type: "PDF",
      icon: <FileText size={20} />,
      date: "3 Days Ago"
    }
  ];

  return (
    <div className="history-page">

      <div className="history-header">

        <h2>History</h2>

      </div>

      <div className="history-search">

        <Search size={18} />

        <input
          type="text"
          placeholder="Search History..."
        />

      </div>

      <div className="filter-buttons">

        <button>All</button>
        <button>Chat</button>
        <button>Quiz</button>
        <button>Interview</button>
        <button>PDF</button>

      </div>

      <div className="history-list">

        {history.map((item, index) => (

          <div
            key={index}
            className="history-card"
          >

            <div className="history-left">

              {item.icon}

              <div>

                <h3>{item.title}</h3>

                <p>{item.date}</p>

              </div>

            </div>

            <span>{item.type}</span>

          </div>

        ))}

      </div>

    </div>
  );
}

export default History;