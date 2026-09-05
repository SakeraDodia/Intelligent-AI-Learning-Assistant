import axios from "axios";

const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 300000,
  headers: {
    "Content-Type": "application/json",
  },
});


// ======================================================
// AI CHAT
// ======================================================

export const sendChatMessage = async (message) => {
  const response = await API.post("/chat", {
    message,
  });

  return response.data;
};


// ======================================================
// QUIZ
// ======================================================

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


// ======================================================
// ROADMAP
// ======================================================

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


// ======================================================
// NOTES
// ======================================================

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


// ======================================================
// INTERVIEW - QUESTION
// ======================================================

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


// ======================================================
// INTERVIEW - EVALUATE ANSWER
// ======================================================

export const evaluateInterviewAnswer = async (
  topic,
  question,
  answer,
  level = "beginner"
) => {

  const response = await API.post(
    "/interview/evaluate",
    {
      topic,
      question,
      answer,
      level,
    }
  );

  return response.data;
};


// ======================================================
// PDF UPLOAD
// ======================================================

export const uploadPDF = async (file) => {

  const formData = new FormData();

  formData.append("file", file);

  const response = await API.post(
    "/pdf/upload",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
};


// ======================================================
// PDF CHAT
// ======================================================

export const sendPDFMessage = async (
  sessionId,
  message
) => {

  const response = await API.post(
    "/pdf/chat",
    {
      session_id: sessionId,
      message,
    }
  );

  return response.data;
};


export default API;