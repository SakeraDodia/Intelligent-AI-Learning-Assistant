import "./ResetPassword.css";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../services/api";

function ResetPassword() {

  const navigate = useNavigate();

  const [password, setPassword] =
    useState("");

  const [confirmPassword,
    setConfirmPassword] =
    useState("");

  const email =
    localStorage.getItem(
      "resetEmail"
    );

  const handleResetPassword =
    async (e) => {

      e.preventDefault();

      if (
        password !==
        confirmPassword
      ) {

        alert(
          "Passwords do not match"
        );

        return;
      }

      try {

        await api.post(
          "/auth/reset-password",
          {
            email,
            new_password:
              password
          }
        );

        localStorage.removeItem(
          "resetEmail"
        );

        alert(
          "Password Updated Successfully"
        );

        navigate("/");

      } catch (error) {

        alert(
          error.response?.data?.detail
        );

      }
    };

  return (
    <div className="forgot-page">

      <div className="forgot-card">

        <h1>Reset Password</h1>

        <p>
          Create a new password
        </p>

        <form
          onSubmit={
            handleResetPassword
          }
        >

          <input
            type="password"
            placeholder="New Password"
            value={password}
            onChange={(e) =>
              setPassword(
                e.target.value
              )
            }
          />

          <input
            type="password"
            placeholder="Confirm Password"
            value={confirmPassword}
            onChange={(e) =>
              setConfirmPassword(
                e.target.value
              )
            }
          />

          <button type="submit">
            Reset Password
          </button>

        </form>

      </div>

    </div>
  );
}

export default ResetPassword;