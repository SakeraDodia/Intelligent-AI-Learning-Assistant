import "./Interview.css";

import { useState } from "react";

import {
  Mic,
  Play,
  Bot,
  User,
  Trophy
} from "lucide-react";

import {
  generateInterviewQuestion,
  evaluateInterviewAnswer
} from "../../services/api";

function Interview() {

  const [screen, setScreen] =
    useState("start");

  const [topic, setTopic] =
    useState("");

  const [level, setLevel] =
    useState("beginner");

  const [question, setQuestion] =
    useState("");

  const [answer, setAnswer] =
    useState("");

  const [messages, setMessages] =
    useState([]);

  const [previousQuestions, setPreviousQuestions] =
    useState([]);

  const [feedback, setFeedback] =
    useState("");

  const [score, setScore] =
    useState(null);

  const [loading, setLoading] =
    useState(false);


  // ======================================================
  // START INTERVIEW
  // ======================================================

  const handleStartInterview = async () => {

    if (!topic.trim() || loading) {
      return;
    }

    setLoading(true);

    try {

      const data =
        await generateInterviewQuestion(
          topic,
          level,
          []
        );

      const newQuestion =
        data.question ||
        data.response ||
        data.content ||
        "";

      setQuestion(newQuestion);

      setPreviousQuestions([
        newQuestion
      ]);

      setMessages([
        {
          sender: "ai",
          text: newQuestion
        }
      ]);

      setAnswer("");

      setScreen("chat");

    } catch (error) {

      console.error(
        "Interview API Error:",
        error
      );

      alert(
        "Unable to start interview. Please check the backend."
      );

    } finally {

      setLoading(false);

    }
  };


  // ======================================================
  // SUBMIT ANSWER
  // ======================================================

  const handleSubmitAnswer = async () => {

    if (!answer.trim() || loading) {
      return;
    }

    setLoading(true);

    const userAnswer =
      answer.trim();

    try {

      // Add user answer to UI
      setMessages((prev) => [
        ...prev,
        {
          sender: "user",
          text: userAnswer
        }
      ]);


      // Evaluate answer
      const evaluation =
        await evaluateInterviewAnswer(
          topic,
          question,
          userAnswer,
          level
        );


      const feedbackText =
        evaluation.feedback ||
        evaluation.response ||
        evaluation.evaluation ||
        "";


      const evaluationScore =
        evaluation.score;


      setFeedback(feedbackText);

      if (
        evaluationScore !== undefined
      ) {

        setScore(
          evaluationScore
        );

      }


      // Generate next question

      const nextData =
        await generateInterviewQuestion(
          topic,
          level,
          previousQuestions
        );


      const nextQuestion =
        nextData.question ||
        nextData.response ||
        nextData.content ||
        "";


      setQuestion(nextQuestion);


      setPreviousQuestions(
        (prev) => [
          ...prev,
          nextQuestion
        ]
      );


      setMessages((prev) => [
        ...prev,
        {
          sender: "ai",
          text: nextQuestion
        }
      ]);


      setAnswer("");

    } catch (error) {

      console.error(
        "Interview Error:",
        error
      );

      alert(
        "Unable to process interview answer."
      );

    } finally {

      setLoading(false);

    }
  };


  // ======================================================
  // REPORT
  // ======================================================

  const handleCompleteInterview = () => {

    setScreen("report");

  };


  // ======================================================
  // RESET
  // ======================================================

  const handleStartAgain = () => {

    setScreen("start");

    setTopic("");

    setQuestion("");

    setAnswer("");

    setMessages([]);

    setPreviousQuestions([]);

    setFeedback("");

    setScore(null);

  };


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
            value={topic}
            onChange={(e) =>
              setTopic(e.target.value)
            }
          />


          <select
            value={level}
            onChange={(e) =>
              setLevel(e.target.value)
            }
          >

            <option value="beginner">
              Beginner
            </option>

            <option value="intermediate">
              Intermediate
            </option>

            <option value="advanced">
              Advanced
            </option>

          </select>


          <button
            onClick={
              handleStartInterview
            }
            disabled={
              loading ||
              !topic.trim()
            }
          >

            <Play size={18} />

            {loading
              ? "Starting..."
              : "Start Interview"}

          </button>

        </div>

      )}


      {/* INTERVIEW SCREEN */}

      {screen === "chat" && (

        <div className="interview-chat">


          <div className="chat-header">

            <h2>
              {topic} Interview
            </h2>

            <span>
              AI Interview
            </span>

          </div>


          <div className="messages">

            {messages.map(
              (msg, index) => (

                <div
                  key={index}
                  className={`message ${msg.sender}`}
                >

                  <div className="icon">

                    {msg.sender === "user" ? (
                      <User size={18} />
                    ) : (
                      <Bot size={18} />
                    )}

                  </div>


                  <div className="bubble">

                    {msg.text}

                  </div>

                </div>

              )
            )}


            {loading && (

              <div className="message ai">

                <div className="icon">

                  <Bot size={18} />

                </div>

                <div className="bubble">

                  AI is thinking...

                </div>

              </div>

            )}

          </div>


          <div className="answer-area">

            <textarea
              placeholder="Type your answer..."
              value={answer}
              disabled={loading}
              onChange={(e) =>
                setAnswer(
                  e.target.value
                )
              }
            />


            <button
              onClick={
                handleSubmitAnswer
              }
              disabled={
                loading ||
                !answer.trim()
              }
            >

              {loading
                ? "Evaluating..."
                : "Submit Answer"}

            </button>


            <button
              onClick={
                handleCompleteInterview
              }
              disabled={loading}
            >

              Complete Interview

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

            {score !== null
              ? `${score}/10`
              : "Completed"}

          </div>


          <div className="skills">

            <div className="skill">

              Technical Skills

              <span>
                {score !== null
                  ? `${score}/10`
                  : "Evaluated"}
              </span>

            </div>


            <div className="skill">

              AI Feedback

              <span>
                {feedback
                  ? "Available"
                  : "Completed"}
              </span>

            </div>

          </div>


          {feedback && (

            <p>
              {feedback}
            </p>

          )}


          <button
            onClick={
              handleStartAgain
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