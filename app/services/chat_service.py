# Business Logic
from app.clients.llm_client import LLMClient, LLMClientError
from app.core.config import settings
from app.schemas.chat import ChatResponse
from app.services.session_store import SessionStore


class ChatService:
    def __init__(self, client: LLMClient, store: SessionStore):  # Dependency Injection
        self.client = client
        self.store = store

    def ask(self, session_id: str, user_message: str):
        messages = [
            {"role": "system", "content": settings.system_prompt},
            *self.store.get(session_id),
            {"role": "user", "content": user_message},
        ]

        data = self.client.complete(messages)
        reply = self._extract_text(data)
        if not reply:
            raise LLMClientError("LLM returned no text.")

        self.store.save_exchange(session_id, user_message, reply)

        return ChatResponse(reply=reply, total_tokens=data["usage"]["total_tokens"])
        
    def reset(self, session_id: str):
        self.store.clear(session_id)

    @staticmethod
    def _extract_text(data: dict):
        parts = []
        for item in data["output"]:
            if item["type"] == "message":
                for block in item["content"]:
                    if block["type"] == "output_text":
                        parts.append(block["text"])
        return "".join(parts)
