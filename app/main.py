import logging

from fastapi import FastAPI

from app.api.routes import chat

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Delicious Kitchen Chatbot", swagger_ui_parameters= {"defaultModelsExpandDepth": -1})
app.include_router(chat.router)

@app.get("/health")
def health():
    return {"status":"ok"}