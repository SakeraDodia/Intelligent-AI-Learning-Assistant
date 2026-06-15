import "./Interview.css";

import { useState } from "react";

import {
  Mic,
  Play,
  Bot,
  User,
  Trophy
} from "lucide-react";

function Interview() {

  const [screen, setScreen] =
    useState("start");

  const questions = [
    "Tell me about yourself.",
    "What are React Hooks?",
    "Why do you want this job?"
  ];

  return (

    <div className="interview-page">

      {/* START SCREEN */}

      {screen === "start" && (

        <div className="interview-card">

          <Mic size={70} />

          <h2>
            AI Interview Preparation
          </h2>

          <p>
            Practice mock interviews with AI
          </p>

          <input
            type="text"
            placeholder="Enter Job Role"
          />

          <button
            onClick={() =>
              setScreen("chat")
            }
          >
            <Play size={18} />

            Start Interview

          </button>

        </div>

      )}

      {/* INTERVIEW SCREEN */}

      {screen === "chat" && (

        <div className="interview-chat">

          <div className="chat-header">

            <h2>
              Frontend Developer Interview
            </h2>

            <span>
              Question 1 / 3
            </span>

          </div>

          <div className="messages">

            <div className="message ai">

              <div className="icon">
                <Bot size={18} />
              </div>

              <div className="bubble">
                {questions[0]}
              </div>

            </div>

            <div className="message user">

              <div className="icon">
                <User size={18} />
              </div>

              <div className="bubble">
                I am a React developer...
              </div>

            </div>

          </div>

          <div className="answer-area">

            <textarea
              placeholder="Type your answer..."
            />

            <button
              onClick={() =>
                setScreen("report")
              }
            >
              Submit Answer
            </button>

          </div>

        </div>

      )}

      {/* REPORT SCREEN */}

      {screen === "report" && (

        <div className="report-card">

          <Trophy size={70} />

          <h2>
            Interview Completed
          </h2>

          <div className="score-circle">
            85%
          </div>

          <div className="skills">

            <div className="skill">
              Communication
              <span>8/10</span>
            </div>

            <div className="skill">
              Technical Skills
              <span>9/10</span>
            </div>

            <div className="skill">
              Confidence
              <span>8/10</span>
            </div>

          </div>

          <button
            onClick={() =>
              setScreen("start")
            }
          >
            Start Again
          </button>

        </div>

      )}

    </div>

  );
}

export default Interview;