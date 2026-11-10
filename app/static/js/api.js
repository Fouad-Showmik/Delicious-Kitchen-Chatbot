const GENERIC_ERROR = "Sorry, I couldn't get a reply right now. Please try again.";
const NETWORK_ERROR = "Network problem. Please check your connection and try again.";

// Send one message and return the assistant's reply.
export async function sendMessage(sessionId, message) {
  let response;

  try {
    response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: sessionId, message }),
    });
  } catch {
    throw new Error(NETWORK_ERROR);
  }

  let data;
  try {
    data = await response.json();
  } catch {
    throw new Error(GENERIC_ERROR);
  }

  if (!response.ok) {
    const detail = typeof data?.detail === "string" ? data.detail.trim() : "";
    throw new Error(detail || GENERIC_ERROR);
  }

  if (typeof data?.reply !== "string") {
    throw new Error(GENERIC_ERROR);
  }

  return data.reply;
}

// Try to clear server-side memory without interrupting the new chat flow.
export async function deleteChat(sessionId) {
  try {
    const response = await fetch(`/api/chat/${encodeURIComponent(sessionId)}`, {
      method: "DELETE",
    });

    if (!response.ok) {
      console.warn("Could not clear the previous chat on the server.");
    }
  } catch {
    console.warn("Could not reach the server to clear the previous chat.");
  }
}
