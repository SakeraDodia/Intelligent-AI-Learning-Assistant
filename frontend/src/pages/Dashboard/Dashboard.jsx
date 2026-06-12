import "./Dashboard.css";

import Navbar from "../../components/Navbar/Navbar";
import StatCard from "../../components/StatCard/StatCard";

import {
  MessageSquare,
  FileText,
  Brain,
  Clock,
  Sparkles,
  Upload,
  NotebookPen,
  GraduationCap
} from "lucide-react";

function Dashboard() {

  const stats = [
    {
      title: "AI Chats",
      value: "128",
      growth: "+12%",
      icon: <MessageSquare size={24} />
    },
    {
      title: "PDF Uploaded",
      value: "24",
      growth: "+8%",
      icon: <FileText size={24} />
    },
    {
      title: "Quizzes Generated",
      value: "15",
      growth: "+19%",
      icon: <Brain size={24} />
    },
    {
      title: "Learning Hours",
      value: "36.5",
      growth: "+10%",
      icon: <Clock size={24} />
    }
  ];

  return (
    <div className="dashboard">

      <Navbar />

      {/* Hero Section */}

      <div className="hero-card">

        <div>
          <h1>
            Welcome, Sakera!
          </h1>

          <p>
            Continue learning with AI-powered
            study assistance and smart insights.
          </p>

          <button className="hero-btn">
            Start Learning
          </button>
        </div>

        <div className="hero-icon">
          <Sparkles size={90} />
        </div>

      </div>

      {/* Stats */}

      <div className="stats-grid">

        {stats.map((item, index) => (
          <StatCard
            key={index}
            title={item.title}
            value={item.value}
            growth={item.growth}
            icon={item.icon}
          />
        ))}

      </div>

      {/* Quick Actions */}

      <div className="section">

        <h2>Quick Actions</h2>

        <div className="action-grid">

          <div className="action-card">
            <MessageSquare size={28} />
            <h3>AI Chat</h3>
            <p>Ask AI anything instantly</p>
          </div>

          <div className="action-card">
            <Upload size={28} />
            <h3>Upload PDF</h3>
            <p>Chat with your documents</p>
          </div>

          <div className="action-card">
            <NotebookPen size={28} />
            <h3>Generate Notes</h3>
            <p>Create study notes quickly</p>
          </div>

          <div className="action-card">
            <GraduationCap size={28} />
            <h3>Generate Quiz</h3>
            <p>Test your knowledge</p>
          </div>

        </div>

      </div>

      {/* Bottom Section */}

      <div className="bottom-grid">

        <div className="recent-card">

          <h2>Recent Chats</h2>

          <ul>
            <li>React Hooks Tutorial</li>
            <li>FastAPI Authentication</li>
            <li>Machine Learning Basics</li>
            <li>Prompt Engineering Guide</li>
          </ul>

        </div>

        <div className="recent-card">

          <h2>Recent PDFs</h2>

          <ul>
            <li>React Documentation.pdf</li>
            <li>DSA Notes.pdf</li>
            <li>Python Guide.pdf</li>
            <li>ML Handbook.pdf</li>
          </ul>

        </div>

      </div>

    </div>
  );
}

export default Dashboard;