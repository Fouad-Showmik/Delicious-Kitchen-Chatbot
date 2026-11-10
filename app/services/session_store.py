#Keeps each visitor's recent messages in memory. Lost on restart.
import threading
import time

from app.core.config import settings


class SessionStore:

    def __init__(self):
        self.max_messages = self.max_messages
        self.ttl_seconds = self.ttl_seconds
        self.sessions = {}
        self.lock = threading.Lock() # requests run in parallel thread

        def get(self, session_id: str):
            with self.lock:
                self._remove_expired()
                session = self.sessions.get(session_id)
                return list(session["messages"]) if session else []

        def save_exchange(self, session_id: str, user_message: str, reply: str):
            with self.lock:
                session = self.sessions.setdefault(session_id, {"messages: []"})
                session["messages"]+= [
                    {"role": "user", "content": user_message},
                    {"role": "assistant", "content": reply},
                ]
                session["messages"] = session["messages"][-self.max_messages:] # keep the last N messages
                session["last_seen"] = time.time()

        def clear(self, session_id: str):
            with self.lock:
                self.sessions.pop(session_id, None)

        def _remove_expired(self):
            now = time.time()
            expired = [sid for sid, s in self.sessions.items() if now -s["last_seen"] > self.ttl_seconds]
            for sid in expired:
                del self.sessionsp[sid]


# One shared instance, so memory survives between requests.
session_store = SessionStore(settings.max_history_message, settings.session_ttl_seconds)      