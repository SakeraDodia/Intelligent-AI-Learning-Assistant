import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
  timeout: 120000,
  headers: {
    "Content-Type": "application/json",
  },
});

// ==============================
// AI CHAT
// ==============================
export const sendChatMessage = async (message) => {
  const response = await API.post("/chat", {
    message,
  });

  return response.data;
};

// ==============================
// QUIZ
// ==============================
export const generateQuiz = async (
  topic,
  difficulty = "medium",
  numberOfQuestions = 5
) => {
  const response = await API.post("/quiz", {
    topic,
    difficulty,
    number_of_questions: numberOfQuestions,
  });

  return response.data;
};

// ==============================
// ROADMAP
// ==============================
export const generateRoadmap = async (
  topic,
  currentLevel,
  studyTime,
  duration
) => {
  const response = await API.post("/roadmap", {
    topic,
    current_level: currentLevel,
    study_time: studyTime,
    duration,
  });

  return response.data;
};

// ==============================
// NOTES
// ==============================
export const generateNotes = async (
  topic,
  level = "beginner"
) => {
  const response = await API.post("/notes", {
    topic,
    level,
  });

  return response.data;
};

// ==============================
// INTERVIEW
// ==============================
export const generateInterviewQuestion = async (
  topic,
  level = "beginner",
  previousQuestions = []
) => {
  const response = await API.post("/interview", {
    topic,
    level,
    previous_questions: previousQuestions,
  });

  return response.data;
};

export default API;