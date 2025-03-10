// static/js/chatbot.js

class ChatBot {
  constructor() {
    console.log("Initializing ChatBot...");
    this.baseUrl = `${window.location.protocol}//${window.location.host}`;
    this.messagesContainer = document.getElementById("messages");
    this.inputField = document.getElementById("user-input");
    this.sendButton = document.getElementById("send-btn");

    if (!this.messagesContainer || !this.inputField || !this.sendButton) {
      console.error("Chatbot UI elements not found!");
      return;
    }

    this.setupEventListeners();
    this.loadMessages();
    this.setupQuickActions();
  }

  setupEventListeners() {
    this.sendButton.addEventListener("click", () => this.sendMessage());
    this.inputField.addEventListener("keypress", (e) => {
      if (e.key === "Enter") {
        this.sendMessage();
      }
    });
  }

  setupQuickActions() {
    const quickActions = [
      { label: "Continue Learning", action: "continue-learning" },
      { label: "Run Security Check", action: "run-assessment" },
      { label: "Test My Skills", action: "test-skills" },
    ];

    const quickActionsContainer = document.createElement("div");
    quickActionsContainer.className = "quick-actions";

    quickActions.forEach((action) => {
      const button = document.createElement("button");
      button.className = "btn btn-secondary me-2 mb-2";
      button.textContent = action.label;
      button.onclick = () => this.handleQuickAction(action.action);
      quickActionsContainer.appendChild(button);
    });

    this.messagesContainer.parentElement.insertBefore(
      quickActionsContainer,
      this.messagesContainer
    );
  }

  handleQuickAction(action) {
    const actions = {
      "continue-learning": () =>
        this.sendMessage("Continue my security training"),
      "run-assessment": () => this.sendMessage("Start security assessment"),
      "test-skills": () => this.sendMessage("Test my security skills"),
    };
    if (actions[action]) {
      actions[action]();
    }
  }

  async sendMessage(predefinedMessage = null) {
    const message = predefinedMessage || this.inputField.value.trim();
    if (!message) return;

    this.addMessage("user", message);
    this.inputField.value = "";

    // Show typing indicator while waiting for response
    const typingIndicator = this.showTypingIndicator();

    try {
      const response = await fetch(`${this.baseUrl}/chatbot/respond/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": this.getCSRFToken(),
        },
        body: JSON.stringify({ message }),
      });

      if (!response.ok)
        throw new Error(`HTTP error! Status: ${response.status}`);

      const data = await response.json();
      this.messagesContainer.removeChild(typingIndicator);
      this.addMessage("bot", data.response);
    } catch (error) {
      this.messagesContainer.removeChild(typingIndicator);
      this.addMessage(
        "bot",
        "Sorry, I encountered an error. Please try again."
      );
    }
  }

  showTypingIndicator() {
    const typingDiv = document.createElement("div");
    typingDiv.className = "message bot typing-indicator";
    typingDiv.innerHTML = `<span>...</span>`;
    this.messagesContainer.appendChild(typingDiv);
    this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    return typingDiv;
  }

  addMessage(sender, message) {
    if (!this.messagesContainer) {
      console.error("Error: messagesContainer is null");
      return;
    }

    // Create message wrapper
    const messageWrapper = document.createElement("div");
    messageWrapper.classList.add(
      "message-wrapper",
      sender === "user" ? "user-message" : "bot-message"
    );

    // Create message div
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", sender);
    messageDiv.innerHTML = this.formatMessage(message);

    // Avatar logic
    if (sender === "bot") {
      const avatarImg = document.createElement("img");
      avatarImg.src = "/static/images/bot-avatar.png"; // Make sure the path is correct
      avatarImg.classList.add("avatar", "bot-avatar");
      messageWrapper.appendChild(avatarImg);
    }

    // Append message to wrapper
    messageWrapper.appendChild(messageDiv);
    this.messagesContainer.appendChild(messageWrapper);

    // Scroll to the latest message
    this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
  }

  formatMessage(message) {
    // Ensure line breaks are properly formatted
    message = message.replace(/\n/g, "<br>");

    // Convert markdown-like `**bold**` text to HTML <strong>
    message = message.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");

    // Convert `*item*` bullet points into HTML lists
    message = message.replace(
      /(\* \*\*(.*?)\*\*:)/g,
      "<br><strong>$2:</strong><ul>"
    );
    message = message.replace(/(\* (?!\*\*)(.*?))/g, "<li>$2</li>");
    message = message.replace(/<\/ul>\n/g, "</ul>"); // Remove unnecessary new lines in lists

    // Wrap bullets inside <ul> if detected
    if (message.includes("<li>")) {
      message = message.replace(
        /<br><strong>(.*?)<\/strong><ul>/g,
        "<br><br><strong>$1</strong><ul>"
      );
    }

    return message;
  }

  async loadMessages() {
    try {
      const response = await fetch(`${this.baseUrl}/chatbot/messages/`);
      if (!response.ok) throw new Error("Failed to fetch messages");

      const data = await response.json();
      this.messagesContainer.innerHTML = ""; // Clear existing messages

      data.messages.forEach((msg) => {
        this.addMessage(msg.sender, msg.message);
      });
    } catch (error) {
      this.addMessage("bot", "Failed to load messages. Please try again.");
    }
  }

  getCSRFToken() {
    const csrfToken = document.querySelector("input[name=csrfmiddlewaretoken]");
    return csrfToken ? csrfToken.value : "";
  }
}

// Initialize chatbot after DOM is fully loaded
document.addEventListener("DOMContentLoaded", () => {
  new ChatBot();
});
