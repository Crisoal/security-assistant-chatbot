import { useState } from "react";

import "./App.css";
import SignIn from "./components/SignIn"; 
import SignUp from "./components/Signup";  
import "./components/Auth.css";

const App: React.FC = () => {
  const [showSignUp, setShowSignUp] = useState(true);

  return (
    <div>
      <h1>Authentication</h1>
      <button onClick={() => setShowSignUp(!showSignUp)}>
        {showSignUp ? "Switch to Sign In" : "Switch to Sign Up"}
      </button>

      {/* Ensure the components are correctly used */}
      {showSignUp ? <SignUp /> : <SignIn />}
    </div>
  );
};

export default App;
