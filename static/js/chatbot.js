// static/js/chatbot.js
class ChatBot {
    constructor() {
        console.log("Initializing ChatBot...");
        this.messagesContainer = document.getElementById("messages");
        this.inputField = document.getElementById("user-input");
        this.sendButton = document.getElementById("send-btn");
        this.welcomeMessage = document.getElementById("welcome-message");
        this.quickActions = document.getElementById("quick-actions");
        this.chatbox = document.getElementById("chatbox");
        this.chatContainer = document.querySelector(".chat-container");
        this.inputContainer = document.querySelector(".input-container");

        if (!this.messagesContainer || !this.inputField || !this.sendButton) {
            console.error("Chatbot UI elements not found!");
            return;
        }

        this.setupEventListeners();
        this.loadMessages();
    }

    setupEventListeners() {
        this.sendButton.addEventListener("click", () => this.sendMessage());
        this.inputField.addEventListener("keypress", (e) => {
            if (e.key === "Enter") {
                this.sendMessage();
            }
        });

        // Quick Actions Event Listener
        document.querySelectorAll(".action-btn").forEach((button) => {
            button.addEventListener("click", (event) => {
                const action = event.target.getAttribute("data-action");
                this.handleQuickAction(action);
            });
        });

        // Expand chatbot on typing
        this.inputField.addEventListener("focus", () => this.expandChat());
    }

    expandChat() {
        this.chatContainer.style.height = "70vh";
        this.chatbox.style.display = "block";
        this.inputContainer.style.position = "fixed";
        this.inputContainer.style.bottom = "0";
        this.inputContainer.style.width = "60%";
        this.inputContainer.style.maxWidth = "600px";

        // Hide welcome message and quick actions
        this.welcomeMessage.style.display = "none";
        this.quickActions.style.opacity = "0";
        setTimeout(() => {
            this.quickActions.style.display = "none";
        }, 400);
    }

    async sendMessage(predefinedMessage = null) {
        const message = predefinedMessage || this.inputField.value.trim();
        if (!message) return;

        this.addMessage("user", message);
        this.inputField.value = "";

        // Hide quick actions after sending message
        this.quickActions.style.display = "none";

        // Show typing indicator while waiting for response
        const typingIndicator = this.showTypingIndicator();
        try {
            const response = await fetch("/chatbot/respond/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": this.getCSRFToken(),
                },
                body: JSON.stringify({ message }),
            });

            if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
            const data = await response.json();

            this.messagesContainer.removeChild(typingIndicator);

            if (data.response) {
                this.addMessage("bot", data.response);
            }
        } catch (error) {
            this.messagesContainer.removeChild(typingIndicator);
            this.addMessage("bot", "Sorry, I encountered an error. Please try again.");
        }
    }

    handleQuickAction(action) {
        let message = "";
        if (action === "continue-learning") {
            message = "I'd like to continue my learning path.";
        } else if (action === "run-security-check") {
            message = "Run a security check for me.";
        } else if (action === "test-my-skills") {
            message = "I want to test my security skills.";
        }

        this.sendMessage(message);
    }

    addMessage(sender, message) {
        const messageWrapper = document.createElement("div");
        messageWrapper.classList.add("message-wrapper", sender === "user" ? "user-message" : "bot-message");

        const messageDiv = document.createElement("div");
        messageDiv.classList.add("message", sender);
        messageDiv.innerHTML = message;

        messageWrapper.appendChild(messageDiv);
        this.messagesContainer.appendChild(messageWrapper);
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }

    showTypingIndicator() {
        const typingDiv = document.createElement("div");
        typingDiv.className = "message bot typing-indicator";
        typingDiv.innerHTML = `<span>...</span>`;
        this.messagesContainer.appendChild(typingDiv);
        return typingDiv;
    }

    getCSRFToken() {
        return document.querySelector("input[name=csrfmiddlewaretoken]")?.value || "";
    }
}

document.addEventListener("DOMContentLoaded", () => {
    new ChatBot();
});

// Theme Toggle Functionality
document.addEventListener("DOMContentLoaded", function () {
    const themeToggle = document.getElementById("theme-toggle");
    const body = document.body;
    
    // Check local storage for theme preference
    if (localStorage.getItem("theme") === "light") {
        body.classList.add("light-theme");
        themeToggle.innerHTML = '<i class="fa-solid fa-sun"></i>';
    }

    themeToggle.addEventListener("click", function () {
        body.classList.toggle("light-theme");
        
        if (body.classList.contains("light-theme")) {
            localStorage.setItem("theme", "light");
            themeToggle.innerHTML = '<i class="fa-solid fa-sun"></i>';
        } else {
            localStorage.setItem("theme", "dark");
            themeToggle.innerHTML = '<i class="fa-solid fa-moon"></i>';
        }
    });
});
