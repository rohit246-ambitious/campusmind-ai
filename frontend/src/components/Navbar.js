import React from "react";
import { useNavigate } from "react-router-dom";

function Navbar() {
  const navigate = useNavigate();

  const logout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  return (
    <div style={{
      display: "flex",
      gap: "10px",
      padding: "10px",
      background: "#222",
      color: "#fff"
    }}>
      <button onClick={() => navigate("/dashboard")}>Dashboard</button>
      <button onClick={() => navigate("/create-issue")}>Create Issue</button>
      <button onClick={() => navigate("/chatbot")}>Chatbot</button>
      <button onClick={() => navigate("/study-planner")}>Study Planner</button>

      <button onClick={logout} style={{ marginLeft: "auto" }}>
        Logout
      </button>
    </div>
  );
}

export default Navbar;