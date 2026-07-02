import "./Profile.css";

import {
  User,
  Mail,
  GraduationCap,
  Code
} from "lucide-react";

function Profile() {

  return (

    <div className="profile-page">

      <div className="profile-card">

        <div className="profile-avatar">

          SD

        </div>

        <h2>
          Sakera Dodia
        </h2>

        <p>
          React Developer
        </p>

      </div>

      <div className="profile-form">

        <div className="input-group">

          <User size={18}/>

          <input
            type="text"
            value="Sakera Dodia"
          />

        </div>

        <div className="input-group">

          <Mail size={18}/>

          <input
            type="email"
            value="example@gmail.com"
          />

        </div>

        <div className="input-group">

          <GraduationCap size={18}/>

          <input
            type="text"
            value="BCA"
          />

        </div>

        <div className="input-group">

          <Code size={18}/>

          <input
            type="text"
            value="React, FastAPI"
          />

        </div>

        <button>
          Save Profile
        </button>

      </div>

    </div>
  );
}

export default Profile;