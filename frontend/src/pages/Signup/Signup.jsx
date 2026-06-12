import "./Signup.css";
import api from "../../services/api";
import { Link, useNavigate } from "react-router-dom";

import { MdOutlineMail } from "react-icons/md";
import { FiLock } from "react-icons/fi";
import { FaBrain, FaUser } from "react-icons/fa";
import { RiRobot2Fill } from "react-icons/ri";

import robot from "../../assets/images/robot.png";
import { useState } from "react";

function Signup() {
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const handleSignup = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post(
        "/auth/signup",
        {
          name,
          email,
          password
        }
      );

      console.log("Signup Success:", response.data);

      navigate("/");

    } catch (error) {
      console.log("Signup Error:", error.response?.data);
      console.log(error);
    }
  };

  return (
    <div className="signup-page">

      {/* LEFT PANEL */}

      <div className="left-panel">

        <div className="brand">
          <div className="logo-container">
            <FaBrain className="logo-icon" />
          </div>

          <div>
            <h1>AI Learning Assistant</h1>
          </div>
        </div>

        <p className="hero-text">
          Join the next generation learning platform
          powered by Artificial Intelligence.
        </p>

        <img
          src={robot}
          alt="robot"
          className="robot-image"
        />

      </div>

      {/* RIGHT PANEL */}

      <div className="right-panel">

        <div className="signup-card">

          <div className="welcome-row">
            <h2>Create Account</h2>
            <RiRobot2Fill className="welcome-icon" />
          </div>

          <p className="subtitle">
            Start your AI learning journey today
          </p>

          <form onSubmit={handleSignup}>
            <label>Full Name</label>

            <div className="input-box">
              <FaUser className="input-icon" />
              <input
                type="text"
                placeholder="Enter your full name"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </div>

            <label>Email Address</label>

            <div className="input-box">
              <MdOutlineMail className="input-icon" />
              <input
                type="email"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>

            <label>Password</label>

            <div className="input-box">
              <FiLock className="input-icon" />
              <input
                type="password"
                placeholder="Create password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>

            <label>Confirm Password</label>

            <div className="input-box">
              <FiLock className="input-icon" />
              <input
                type="password"
                placeholder="Confirm password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
              />
            </div>

            <button type="submit" className="signup-btn">
              Create Account
            </button>

          </form>

          <p className="login-link">
            Already have an account?
            <Link to="/"> Login</Link>
          </p>

        </div>

      </div>

    </div>
  );
}

export default Signup;