import "./Login.css";
import logo from "../../assets/images/logo.png";
import robot from "../../assets/images/robot.png";
import { FaGoogle, FaGithub } from "react-icons/fa";
import { Link, useNavigate } from "react-router-dom";
import { FaBrain } from "react-icons/fa";

function Login() {
  const navigate = useNavigate();

  const handleLogin = () => {
    navigate("/dashboard");
  };

  return (
    <div className="login-page">
      {/* Left Section */}
      <div className="login-left">
        <div className="brand">
          <div className="logo-container">
            <FaBrain className="logo-icon" />
          </div>

          <div>
            <h1>AI Learning Assistant</h1>
            <span className="brand-subtitle">
              Intelligent Learning Platform
            </span>
          </div>
        </div>

        <p className="description">
          Your intelligent companion for learning, exploring and
          achieving more with AI technologies.
        </p>

        <img
          src={robot}
          alt="AI Assistant"
          className="robot-image"
        />
      </div>

      {/* Right Section */}
      <div className="login-right">
        <div className="login-card">

          <h2 className="welcome-title">
            Welcome Back!
          </h2>
          <p className="subtitle">
            Login to continue your learning journey
          </p>

          <form>
            <div className="input-group">
              <label>Email Address</label>
              <input
                type="email"
                placeholder="Enter your email"
              />
            </div>

            <div className="input-group">
              <div className="password-label">
                <label>Password</label>
                <Link to="/forgot-password">Forgot Password?</Link>
              </div>

              <input
                type="password"
                placeholder="Enter your password"
              />
            </div>

            <button type="submit" className="login-btn" >
              Login
            </button>
          </form>

          <div className="divider">
            <span>or continue with</span>
          </div>

          <div className="social-buttons">
            <button className="social-btn">
              <FaGoogle />
              Google
            </button>

            <button className="social-btn">
              <FaGithub />
              GitHub
            </button>
          </div>

          <p className="signup-text">
            Don't have an account?
            <Link to="/signup"> Sign Up</Link>
          </p>
        </div>
      </div>
    </div>
  );
}

export default Login;