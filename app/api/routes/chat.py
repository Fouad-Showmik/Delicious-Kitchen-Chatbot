from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path

from app.clients.llm_client import LLMClient, LLMClientError
from app.schemas.chat import SESSION_ID_PATTERN, ChatRequest, ChatResponse
from app.services.chat_service import ChatService
from app.services.session_store import session_store

router = APIRouter(prefix="/api/chat", tags=["chat"])


def get_chat_service():
    return ChatService(LLMClient(), session_store)


ChatServiceDep = Annotated[ChatService, Depends(get_chat_service)]
SessionIdDep = Annotated[str, Path(pattern=SESSION_ID_PATTERN)]


@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest, service: ChatServiceDep):
    try:
        return service.ask(request.session_id, request.message)
    except LLMClientError:
        raise HTTPException(status_code=502, detail="Sorry, I'm having trouble right now. Please try again.")


@router.delete("/{session_id}", status_code=204)
def reset_chat(service: ChatServiceDep, session_id: SessionIdDep):
    service.reset(session_id)