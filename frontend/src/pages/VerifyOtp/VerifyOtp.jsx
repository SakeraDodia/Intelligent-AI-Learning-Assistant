import "./VerifyOtp.css";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../services/api";

function VerifyOtp() {

  const navigate = useNavigate();

  const [otp, setOtp] = useState("");

  const email =
    localStorage.getItem(
      "resetEmail"
    );

  const handleVerifyOtp = async (e) => {

    e.preventDefault();

    try {

      await api.post(
        "/auth/verify-otp",
        {
          email,
          otp
        }
      );

      navigate("/reset-password");

    } catch (error) {

      alert(
        error.response?.data?.detail
      );

    }
  };

  return (
    <div className="forgot-page">

      <div className="forgot-card">

        <h1>Verify OTP</h1>

        <p>
          Enter OTP sent to your email
        </p>

        <form onSubmit={handleVerifyOtp}>

          <input
            type="text"
            placeholder="Enter OTP"
            value={otp}
            onChange={(e) =>
              setOtp(e.target.value)
            }
          />

          <button type="submit">
            Verify OTP
          </button>

        </form>

      </div>

    </div>
  );
}

export default VerifyOtp;