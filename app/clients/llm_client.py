import logging

import requests

from app.core.config import settings

#talk to the provider over HTTP and return raw JSON.

logger = logging.getLogger(__name__)

class LLMClientError(Exception):
    pass

class LLMClient: 
    def __init__(self):
        self.url = f"{settings.llm_base_url}/responses"
        self.headers = {
            "Authorization": f"Bearer {settings.llm_api_key}",
            "Content-Type": "application/json",
        }

    def complete(self, messages: list[dict]):
        payload = {
            "model" : settings.model_name,
            "input" : messages,
        }

        try:
            response = requests.post(self.url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()
        
        except requests.RequestException as exc:
            logger.exception("")
            raise LLMClientError(str(exc)) from exc
            