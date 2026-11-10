const SESSION_STORAGE_KEY = "sid";

// Get the conversation id for this tab, creating it when needed.
export function getSessionId() {
  let sessionId = sessionStorage.getItem(SESSION_STORAGE_KEY);

  if (!sessionId) {
    sessionId = crypto.randomUUID();
    sessionStorage.setItem(SESSION_STORAGE_KEY, sessionId);
  }

  return sessionId;
}

// Start a fresh conversation in this tab.
export function resetSessionId() {
  sessionStorage.removeItem(SESSION_STORAGE_KEY);
  return getSessionId();
}
