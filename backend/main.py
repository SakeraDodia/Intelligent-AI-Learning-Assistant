from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from services.chat import chat
from services.quiz import generate_quiz
from services.roadmap import generate_roadmap
from services.notes import generate_notes
from services.interview import generate_interview_question


app = FastAPI(
    title="Intelligent AI Learning Assistant"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# ============================================================
# REQUEST MODELS
# ============================================================

class ChatRequest(BaseModel):
    message: str


class QuizRequest(BaseModel):
    topic: str
    difficulty: str = "medium"
    number_of_questions: int = 5


class RoadmapRequest(BaseModel):
    topic: str
    current_level: str
    study_time: str
    duration: str


class NotesRequest(BaseModel):
    topic: str
    level: str = "beginner"


class InterviewRequest(BaseModel):
    topic: str
    level: str = "beginner"
    previous_questions: list[str] = []


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {
        "status": "running",
        "model": "Qwen2.5-7B-Instruct + QLoRA"
    }


# ============================================================
# CHAT
# ============================================================

@app.post("/chat")
def chat_endpoint(request: ChatRequest):

    response = chat(
        request.message
    )

    return {
        "response": response
    }


# ============================================================
# QUIZ
# ============================================================

@app.post("/quiz")
def quiz_endpoint(request: QuizRequest):

    response = generate_quiz(
        topic=request.topic,
        difficulty=request.difficulty,
        number_of_questions=request.number_of_questions
    )

    return {
        "response": response
    }


# ============================================================
# ROADMAP
# ============================================================

@app.post("/roadmap")
def roadmap_endpoint(request: RoadmapRequest):

    response = generate_roadmap(
        topic=request.topic,
        current_level=request.current_level,
        study_time=request.study_time,
        duration=request.duration
    )

    return {
        "response": response
    }


# ============================================================
# NOTES
# ============================================================

@app.post("/notes")
def notes_endpoint(request: NotesRequest):

    response = generate_notes(
        topic=request.topic,
        level=request.level
    )

    return {
        "response": response
    }


# ============================================================
# INTERVIEW
# ============================================================

@app.post("/interview")
def interview_endpoint(request: InterviewRequest):

    response = generate_interview_question(
        topic=request.topic,
        level=request.level,
        previous_questions=request.previous_questions
    )

    return {
        "response": response
    }