import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import CreateIssue from "./pages/CreateIssue";
import Chatbot from "./pages/Chatbot";
import StudyPlanner from "./pages/StudyPlanner";
import Navbar from "./components/Navbar";

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/create-issue" element={<CreateIssue />} />
        <Route path="/chatbot" element={<Chatbot />} />
        <Route path="/study-planner" element={<StudyPlanner />} />
      </Routes>
    </Router>
  );
}

export default App;