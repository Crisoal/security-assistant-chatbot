import React from "react";
import "../components/Home.css"; // Import the CSS file

const Home: React.FC = () => {
  return (
    <div>
      {/* Navbar */}
      <nav className="navbar">
        <div className="logo">Cybersecurity Chatbot</div>
        <div className="auth-buttons">
          <button
            className="loginButton"
            onClick={() => alert("Login coming soon!")}
          >
            Login
          </button>
          <button
            className="signupButton"
            onClick={() => alert("Sign Up coming soon!")}
          >
            Sign Up
          </button>
        </div>
      </nav>

      {/* Main Content */}
      <div className="container">
        <h1 className="header">Welcome to Cybersecurity Chatbot</h1>
        <p className="description">
          Stay safe online with our AI-powered chatbot. Learn how to protect
          yourself from cyber threats, scams, and social engineering attacks
          through interactive lessons and real-time simulations.
        </p>
      </div>
    </div>
  );
};

export default Home;
