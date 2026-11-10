const GREETING =
  "Assalamu alaikum! Welcome to Delicious Kitchen. Ask me about our menu, delivery areas, timings or policies.";

const messageList = document.querySelector("#message-list");
const quickReplies = document.querySelector("#quick-replies");
const chatForm = document.querySelector("#chat-form");
const messageInput = document.querySelector("#message-input");
const sendButton = document.querySelector("#send-button");
const newChatButton = document.querySelector("#new-chat");

// Add a user, bot, or error bubble and scroll it into view.
export function addBubble(type, text = "") {
  const row = document.createElement("li");
  row.classList.add("message-row", `message-row-${type}`);

  if (type !== "user") {
    const avatar = document.createElement("span");
    avatar.className = "bot-avatar";
    avatar.setAttribute("aria-hidden", "true");

    const avatarImage = document.createElement("img");
    avatarImage.src = "/assets/agents.png";
    avatarImage.alt = "";
    avatar.append(avatarImage);

    row.append(avatar);
  }

  const bubble = document.createElement("div");
  bubble.className = "message-bubble";
  bubble.textContent = text;
  row.append(bubble);
  messageList.append(row);
  scrollToLatest();

  return bubble;
}

// Put the fixed, data-free typing animation inside an existing bot bubble.
export function showTypingIndicator(bubble) {
  bubble.setAttribute("aria-label", "Assistant is typing");
  bubble.innerHTML =
    '<span class="typing-indicator" aria-hidden="true"><span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span></span>';
}

// Replace a pending bubble while keeping its original position in the chat.
export function updateBubble(bubble, type, text) {
  bubble.textContent = text;
  bubble.removeAttribute("aria-label");

  const row = bubble.parentElement;
  row.classList.remove("message-row-bot", "message-row-error");
  row.classList.add(`message-row-${type}`);
  scrollToLatest();
}

// Restore the initial message list and suggested questions.
export function resetChatView() {
  messageList.replaceChildren();
  addBubble("bot", GREETING);
  quickReplies.hidden = false;
  scrollToLatest();
}

// Disable message controls during a pending assistant response.
export function setSending(isSending) {
  messageInput.disabled = isSending;
  sendButton.disabled = isSending;
  newChatButton.disabled = isSending;
  messageInput.setAttribute("aria-busy", String(isSending));
}

// Attach the form, suggested-question, and new-chat handlers.
export function initializeUI({ onSend, onNewChat }) {
  chatForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const message = messageInput.value.trim();

    if (!message || sendButton.disabled) {
      return;
    }

    messageInput.value = "";
    quickReplies.hidden = true;
    onSend(message);
  });

  quickReplies.addEventListener("click", (event) => {
    const button = event.target.closest(".quick-reply");

    if (!button || sendButton.disabled) {
      return;
    }

    quickReplies.hidden = true;
    onSend(button.textContent.trim());
  });

  newChatButton.addEventListener("click", onNewChat);
}

// Keep the newest message visible, including after content is replaced.
function scrollToLatest() {
  messageList.scrollTop = messageList.scrollHeight;
}

// Focus the composer when a reply or error completes.
export function focusMessageInput() {
  messageInput.focus();
}
