import "./Settings.css";

import { useState } from "react";

import {
  Bell,
  Moon,
  Lock,
  LogOut,
  User,
  Shield
} from "lucide-react";

function Settings() {

  const [darkMode, setDarkMode] =
    useState(false);

  const [notifications,
    setNotifications] =
    useState(true);

  return (

    <div className="settings-page">

      <div className="settings-header">

        <h2>Settings</h2>

        <p>
          Manage your account preferences
        </p>

      </div>

      <div className="settings-container">

        <div className="setting-card">

          <div className="setting-left">

            <div className="icon-box">
              <Moon size={18} />
            </div>

            <div>

              <h4>Dark Mode</h4>

              <p>
                Enable dark theme
              </p>

            </div>

          </div>

          <label className="switch">

            <input
              type="checkbox"
              checked={darkMode}
              onChange={() =>
                setDarkMode(
                  !darkMode
                )
              }
            />

            <span className="slider"></span>

          </label>

        </div>

        <div className="setting-card">

          <div className="setting-left">

            <div className="icon-box">
              <Bell size={18} />
            </div>

            <div>

              <h4>
                Email Notifications
              </h4>

              <p>
                Receive updates by email
              </p>

            </div>

          </div>

          <label className="switch">

            <input
              type="checkbox"
              checked={notifications}
              onChange={() =>
                setNotifications(
                  !notifications
                )
              }
            />

            <span className="slider"></span>

          </label>

        </div>

        <div className="setting-card">

          <div className="setting-left">

            <div className="icon-box">
              <Lock size={18} />
            </div>

            <div>

              <h4>
                Change Password
              </h4>

              <p>
                Update your password
              </p>

            </div>

          </div>

        </div>

        <div className="setting-card">

          <div className="setting-left">

            <div className="icon-box">
              <Shield size={18} />
            </div>

            <div>

              <h4>
                Privacy & Security
              </h4>

              <p>
                Manage account security
              </p>

            </div>

          </div>

        </div>

        <div className="setting-card">

          <div className="setting-left">

            <div className="icon-box">
              <User size={18} />
            </div>

            <div>

              <h4>
                Account Details
              </h4>

              <p>
                View account information
              </p>

            </div>

          </div>

        </div>

        <div className="setting-card logout-card">

          <div className="setting-left">

            <div className="icon-box logout-icon">

              <LogOut size={18} />

            </div>

            <div>

              <h4>
                Logout
              </h4>

              <p>
                Sign out of your account
              </p>

            </div>

          </div>

        </div>

      </div>

    </div>

  );
}

export default Settings;