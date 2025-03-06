// static/js/chatbot.js

class ChatBot {
    constructor() {
        this.baseUrl = `${window.location.protocol}//${window.location.host}`;
        this.messagesContainer = document.getElementById('messages');
        this.inputField = document.getElementById('user-input');
        this.sendButton = document.getElementById('send-btn');
        
        this.setupEventListeners();
        this.loadMessages();
    }

    setupEventListeners() {
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.inputField.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
    }

    async sendMessage() {
        const message = this.inputField.value.trim();
        if (!message) return;

        this.addMessage('user', message);
        this.inputField.value = '';
        
        try {
            const response = await fetch(`${this.baseUrl}/chatbot/respond/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({ message })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            this.addMessage('bot', data.response);
        } catch (error) {
            console.error('Error:', error);
            this.addMessage('bot', 'Sorry, I encountered an error. Please try again.');
        }
    }

    addMessage(sender, message) {
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
        try {
            const response = await fetch(`${this.baseUrl}/chatbot/messages/`);
            const messages = await response.json();
            
            messages.forEach(msg => {
                this.addMessage(msg.sender, msg.content);
            });
        } catch (error) {
            console.error('Error loading messages:', error);
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const chatbot = new ChatBot();
});