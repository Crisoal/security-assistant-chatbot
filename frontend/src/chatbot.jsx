import React, { useState } from "react";

const Chatbot = () => {
    const [messages, setMessages] = useState([]);

    const handleUserMessage = (message) => {
        setMessages([...messages, { text: message, user: true }]);
    };

    return (
        <div>
            <h3>Cybersecurity Chatbot</h3>
            <div>
                {messages.map((msg, index) => (
                    <p key={index} style={{ color: msg.user ? "blue" : "black" }}>
                        {msg.text}
                    </p>
                ))}
            </div>
            <input type="text" onKeyDown={(e) => {
                if (e.key === "Enter") {
                    handleUserMessage(e.target.value);
                    e.target.value = "";
                }
            }} />
        </div>
    );
};

export default Chatbot;
