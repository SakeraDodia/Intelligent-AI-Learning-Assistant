import "./Quiz.css";
import { useState } from "react";
import {
  Brain,
  PlayCircle,
  CheckCircle
} from "lucide-react";

function Quiz() {

  const [screen, setScreen] =
    useState("start");

  const questions = [
    {
      question:
        "What is React Hook?",
      options: [
        "State Management",
        "Function",
        "Library",
        "Database"
      ]
    },
    {
      question:
        "Which hook is used for state?",
      options: [
        "useEffect",
        "useMemo",
        "useState",
        "useRef"
      ]
    }
  ];

  return (

    <div className="quiz-page">

      {screen === "start" && (

        <div className="quiz-card">

          <Brain size={70} />

          <h2>
            AI Quiz Generator
          </h2>

          <p>
            Generate quizzes from any topic
          </p>

          <input
            type="text"
            placeholder="Enter Topic"
          />

          <button
            onClick={() =>
              setScreen("quiz")
            }
          >
            <PlayCircle size={18} />

            Generate Quiz
          </button>

        </div>

      )}

      {screen === "quiz" && (

        <div className="quiz-container">

          <div className="quiz-topbar">

            <h2>
              React Fundamentals Quiz
            </h2>

            <span>
              2 Questions
            </span>

          </div>

          {questions.map(
            (item, index) => (

              <div
                key={index}
                className="question-card"
              >

                <h3>
                  {index + 1}.{" "}
                  {item.question}
                </h3>

                <div className="options">

                  {item.options.map(
                    (option, i) => (

                      <label
                        key={i}
                        className="option"
                      >

                        <input
                          type="radio"
                          name={`q${index}`}
                        />

                        {option}

                      </label>

                    )
                  )}

                </div>

              </div>

            )
          )}

          <button
            className="submit-btn"
            onClick={() =>
              setScreen("result")
            }
          >
            Submit Quiz
          </button>

        </div>

      )}

      {screen === "result" && (

        <div className="result-card">

          <CheckCircle size={70} />

          <h2>
            Quiz Completed
          </h2>

          <div className="score-box">
            8 / 10
          </div>

          <p>
            Great Job!
          </p>

          <button
            onClick={() =>
              setScreen("start")
            }
          >
            Start New Quiz
          </button>

        </div>

      )}

    </div>

  );
}

export default Quiz;