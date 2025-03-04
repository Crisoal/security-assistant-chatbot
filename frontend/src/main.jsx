// src/main.jsx
import React from 'react';
import ReactDOM from 'react-dom/client';

// Your app component here
const App = () => {
  return <div>Hello World!</div>;
};

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);