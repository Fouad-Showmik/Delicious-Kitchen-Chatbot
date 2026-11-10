import { deleteChat, sendMessage } from "./api.js";
import { getSessionId, resetSessionId } from "./session.js";
import {
  addBubble,
  focusMessageInput,
  initializeUI,
  resetChatView,
  setSending,
  showTypingIndicator,
  updateBubble,
} from "./ui.js";

let isSending = false;
let sessionId = getSessionId();

// Send the trimmed message and replace its waiting bubble with the result.
async function handleSend(message) {
  if (!message || isSending) {
    return;
  }

  isSending = true;
  setSending(true);
  addBubble("user", message);
  const replyBubble = addBubble("bot");
  showTypingIndicator(replyBubble);

  try {
    const reply = await sendMessage(sessionId, message);
    updateBubble(replyBubble, "bot", reply);
  } catch (error) {
    const messageText =
      error instanceof Error ? error.message : "Something went wrong. Please try again.";
    updateBubble(replyBubble, "error", messageText);
  } finally {
    isSending = false;
    setSending(false);
    focusMessageInput();
  }
}

// Clear server memory, then reset this tab's session and visible conversation.
async function handleNewChat() {
  await deleteChat(sessionId);
  sessionId = resetSessionId();
  resetChatView();
  focusMessageInput();
}

initializeUI({
  onSend: handleSend,
  onNewChat: handleNewChat,
});
resetChatView();
