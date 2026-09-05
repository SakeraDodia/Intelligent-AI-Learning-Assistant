import "./Quiz.css";

import { useState } from "react";

import {
  Brain,
  PlayCircle,
  CheckCircle
} from "lucide-react";

import { generateQuiz } from "../../services/api";

function Quiz() {

  const [screen, setScreen] =
    useState("start");

  const [topic, setTopic] =
    useState("");

  const [difficulty, setDifficulty] =
    useState("medium");

  const [numberOfQuestions, setNumberOfQuestions] =
    useState(5);

  const [questions, setQuestions] =
    useState([]);

  const [answers, setAnswers] =
    useState({});

  const [score, setScore] =
    useState(0);

  const [loading, setLoading] =
    useState(false);


  // ======================================================
  // GENERATE QUIZ
  // ======================================================

  const handleGenerateQuiz = async () => {

    if (!topic.trim() || loading) {
      return;
    }

    setLoading(true);

    try {

      const data = await generateQuiz(
        topic,
        difficulty,
        Number(numberOfQuestions)
      );

      let generatedQuestions =
        data.questions ||
        data.quiz ||
        data.data ||
        [];

      // Handle string response if backend
      // returns generated JSON/text
      if (typeof generatedQuestions === "string") {

        try {

          generatedQuestions =
            JSON.parse(
              generatedQuestions
            );

        } catch {

          console.error(
            "Quiz response is not valid JSON"
          );

        }
      }

      setQuestions(
        Array.isArray(generatedQuestions)
          ? generatedQuestions
          : []
      );

      setAnswers({});

      setScore(0);

      setScreen("quiz");

    } catch (error) {

      console.error(
        "Quiz API Error:",
        error
      );

      alert(
        "Unable to generate quiz. Please check the backend."
      );

    } finally {

      setLoading(false);

    }
  };


  // ======================================================
  // SELECT ANSWER
  // ======================================================

  const handleAnswerChange = (
    questionIndex,
    answer
  ) => {

    setAnswers((prev) => ({
      ...prev,
      [questionIndex]: answer
    }));

  };


  // ======================================================
  // SUBMIT QUIZ
  // ======================================================

  const handleSubmitQuiz = () => {

    let correct = 0;

    questions.forEach(
      (question, index) => {

        const selected =
          answers[index];

        const correctAnswer =
          question.answer ||
          question.correct_answer ||
          question.correctAnswer;

        if (
          selected &&
          correctAnswer &&
          selected.toLowerCase() ===
            String(correctAnswer).toLowerCase()
        ) {

          correct++;

        }

      }
    );

    setScore(correct);

    setScreen("result");
  };


  // ======================================================
  // START SCREEN
  // ======================================================

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
            value={topic}
            onChange={(e) =>
              setTopic(e.target.value)
            }
          />

          <select
            value={difficulty}
            onChange={(e) =>
              setDifficulty(e.target.value)
            }
          >

            <option value="easy">
              Easy
            </option>

            <option value="medium">
              Medium
            </option>

            <option value="hard">
              Hard
            </option>

          </select>

          <input
            type="number"
            min="1"
            max="20"
            value={numberOfQuestions}
            onChange={(e) =>
              setNumberOfQuestions(
                e.target.value
              )
            }
          />

          <button
            onClick={handleGenerateQuiz}
            disabled={
              loading ||
              !topic.trim()
            }
          >

            <PlayCircle size={18} />

            {loading
              ? "Generating..."
              : "Generate Quiz"}

          </button>

        </div>

      )}


      {/* QUIZ SCREEN */}

      {screen === "quiz" && (

        <div className="quiz-container">

          <div className="quiz-topbar">

            <h2>
              {topic} Quiz
            </h2>

            <span>
              {questions.length} Questions
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

                  {(
                    item.options ||
                    item.choices ||
                    []
                  ).map(
                    (option, i) => (

                      <label
                        key={i}
                        className="option"
                      >

                        <input
                          type="radio"
                          name={`q${index}`}
                          value={option}
                          checked={
                            answers[index] ===
                            option
                          }
                          onChange={() =>
                            handleAnswerChange(
                              index,
                              option
                            )
                          }
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
            onClick={handleSubmitQuiz}
          >
            Submit Quiz
          </button>

        </div>

      )}


      {/* RESULT SCREEN */}

      {screen === "result" && (

        <div className="result-card">

          <CheckCircle size={70} />

          <h2>
            Quiz Completed
          </h2>

          <div className="score-box">

            {score} / {questions.length}

          </div>

          <p>

            {score === questions.length
              ? "Excellent!"
              : score >= questions.length / 2
              ? "Great Job!"
              : "Keep Practicing!"}

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