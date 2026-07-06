from fastapi import FastAPI

from app.database import Base
from app.database import engine

from app.models import User

app = FastAPI(
    title="AI Learning Assistant API",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {
        "message": "Backend Running Successfully"
    }