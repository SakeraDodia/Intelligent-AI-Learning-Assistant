from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.auth import router as auth_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth Routes
app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)

@app.get("/")
def home():
    return {
        "message": "AI Learning Assistant Backend"
    }