// static/js/chatbot.js
class ChatBot {
    constructor() {
        console.log("Initializing ChatBot...");

        this.baseUrl = `${window.location.protocol}//${window.location.host}`;
        this.messagesContainer = document.getElementById('messages');
        this.inputField = document.getElementById('user-input');
        this.sendButton = document.getElementById('send-btn');

        console.log("Base URL:", this.baseUrl);
        console.log("Messages Container:", this.messagesContainer);
        console.log("Input Field:", this.inputField);
        console.log("Send Button:", this.sendButton);

        // Check if essential elements exist
        if (!this.messagesContainer || !this.inputField || !this.sendButton) {
            console.error("Chatbot UI elements not found!");
            return;
        }

        this.setupEventListeners();
        this.loadMessages();
        this.setupQuickActions();
    }

    setupEventListeners() {
        console.log("Setting up event listeners...");
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.inputField.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                console.log("Enter key pressed...");
                this.sendMessage();
            }
        });
    }

    setupQuickActions() {
        console.log("Setting up quick actions...");
        const quickActions = [
            { label: 'Continue Learning', action: 'continue-learning' },
            { label: 'Run Security Check', action: 'run-assessment' },
            { label: 'Test My Skills', action: 'test-skills' }
        ];
        const quickActionsContainer = document.createElement('div');
        quickActionsContainer.className = 'quick-actions';

        quickActions.forEach(action => {
            const button = document.createElement('button');
            button.className = 'btn btn-secondary me-2 mb-2';
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
        console.log(`Quick action clicked: ${action}`);
        const actions = {
            'continue-learning': () => this.sendMessage('Continue my security training'),
            'run-assessment': () => this.sendMessage('Start security assessment'),
            'test-skills': () => this.sendMessage('Test my security skills')
        };
        if (actions[action]) {
            actions[action]();
        }
    }

    async sendMessage(predefinedMessage = null) {
        console.log("Sending message...");

        // Ensure inputField exists before reading value
        if (!this.inputField) {
            console.error("Error: inputField is null");
            return;
        }

        const message = predefinedMessage || this.inputField.value.trim();
        console.log("User input:", message);

        if (!message) {
            console.log("No message entered, returning.");
            return;
        }

        this.addMessage('user', message);
        this.inputField.value = '';

        try {
            console.log("Sending request to backend...");
            const response = await fetch(`${this.baseUrl}/chatbot/respond/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({ message })
            });
            

            console.log("Response received:", response);

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            console.log("Backend response:", data);

            this.addMessage('bot', data.response);
        } catch (error) {
            console.error('Error:', error);
            this.addMessage('bot', 'Sorry, I encountered an error. Please try again.');
        }
    }

    addMessage(sender, message) {
        console.log(`Adding message - Sender: ${sender}, Message: ${message}`);

        if (!this.messagesContainer) {
            console.error("Error: messagesContainer is null");
            return;
        }

        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        messageDiv.innerHTML = `
            <div class="message-content">
                ${message}
            </div>
        `;

        this.messagesContainer.appendChild(messageDiv);
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }

    async loadMessages() {
        console.log("Loading previous messages...");

        try {
            const response = await fetch(`${this.baseUrl}/chatbot/messages/`);
            if (!response.ok) throw new Error("Failed to fetch messages");

            const data = await response.json();
            console.log("Loaded messages:", data);

            this.messagesContainer.innerHTML = ''; // Clear existing messages

            data.messages.forEach(msg => {
                this.addMessage(msg.sender, msg.message);
            });
        } catch (error) {
            console.error('Error loading messages:', error);
            this.addMessage('bot', 'Failed to load messages. Please try again.');
        }
    }

    getCSRFToken() {
        const csrfToken = document.querySelector("input[name=csrfmiddlewaretoken]");
        console.log("CSRF Token:", csrfToken ? csrfToken.value : "Not found");
        return csrfToken ? csrfToken.value : '';
    }    
}

// Initialize chatbot after DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log("DOM fully loaded. Initializing ChatBot...");
    new ChatBot();
});
