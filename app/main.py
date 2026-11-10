import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routes import chat

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Delicious Kitchen Chatbot", swagger_ui_parameters= {"defaultModelsExpandDepth": -1})
app.include_router(chat.router)

@app.get("/health")
def health():
    return {"status":"ok"}

app.mount("/", StaticFiles(directory=Path(__file__).parent / "static", html=True))