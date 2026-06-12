import "./Navbar.css";

import { Bell, Search } from "lucide-react";

function Navbar() {
  return (
    <div className="navbar">

      <div className="search-box">
        <Search size={18} />

        <input
          type="text"
          placeholder="Search courses, notes, PDFs..."
        />
      </div>

      <div className="navbar-right">

        <button className="notification-btn">
          <Bell size={20} />
          <span className="notification-dot"></span>
        </button>

        <div className="profile-section">

          <img
            src="https://i.pravatar.cc/150?img=12"
            alt="profile"
          />

          <div>
            <h4>Sakera</h4>
            <span>AI Learner</span>
          </div>

        </div>

      </div>

    </div>
  );
}

export default Navbar;