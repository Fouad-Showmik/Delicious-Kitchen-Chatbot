import logging
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from slowapi.errors import RateLimitExceeded

from app.api.routes import chat
from app.core.limiter import limiter

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Delicious Kitchen Chatbot", swagger_ui_parameters= {"defaultModelsExpandDepth": -1})


#Register the limiter and return a friendly 429 message.
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "You're sending messages too fast. Please wait a moment and try again."},
    )

app.include_router(chat.router)


# GET and HEAD
@app.api_route("/health", methods=["GET","HEAD"])
def health():
    return {"status":"ok"}

app.mount("/", StaticFiles(directory=Path(__file__).parent / "static", html=True))