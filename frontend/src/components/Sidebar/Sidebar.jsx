import "./Sidebar.css";

import { NavLink, useNavigate } from "react-router-dom";
import { useState } from "react";

import Logout from "../Logout/Logout";

import {
  LayoutDashboard,
  MessageSquare,
  FileText,
  NotebookPen,
  Brain,
  Briefcase,
  Map,
  History,
  User,
  Settings,
  LogOut,
} from "lucide-react";

function Sidebar() {
  const [openLogout, setOpenLogout] = useState(false);

  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");

    setOpenLogout(false);

    navigate("/");
  };

  const menuItems = [
    {
      name: "Dashboard",
      icon: <LayoutDashboard size={18} />,
      path: "/dashboard",
    },
    {
      name: "AI Chat",
      icon: <MessageSquare size={18} />,
      path: "/chat",
    },
    {
      name: "PDF Chat",
      icon: <FileText size={18} />,
      path: "/pdf-chat",
    },
    {
      name: "Notes",
      icon: <NotebookPen size={18} />,
      path: "/notes",
    },
    {
      name: "Quiz Generator",
      icon: <Brain size={18} />,
      path: "/quiz",
    },
    {
      name: "Interview Prep",
      icon: <Briefcase size={18} />,
      path: "/interview",
    },
    {
      name: "Roadmap",
      icon: <Map size={18} />,
      path: "/roadmap",
    },
    {
      name: "History",
      icon: <History size={18} />,
      path: "/history",
    },
    {
      name: "Profile",
      icon: <User size={18} />,
      path: "/profile",
    },
    {
      name: "Settings",
      icon: <Settings size={18} />,
      path: "/settings",
    },
  ];

  return (
    <aside className="sidebar">

      <div className="sidebar-logo">
        <div className="logo-box">🤖</div>

        <div className="logo-text">
          <h3>AI Learning</h3>
          <span>Assistant</span>
        </div>
      </div>

      <nav className="sidebar-menu">

        {menuItems.map((item) => (
          <NavLink
            key={item.name}
            to={item.path}
            className={({ isActive }) =>
              isActive
                ? "menu-item active"
                : "menu-item"
            }
          >
            {item.icon}
            <span>{item.name}</span>
          </NavLink>
        ))}

      </nav>

      <button
        className="logout-btn"
        onClick={() => setOpenLogout(true)}
      >
        <LogOut size={18} />
        <span>Logout</span>
      </button>

      <Logout
        isOpen={openLogout}
        onClose={() => setOpenLogout(false)}
        onConfirm={handleLogout}
      />

    </aside>
  );
}

export default Sidebar;