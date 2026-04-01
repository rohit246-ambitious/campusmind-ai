import React, { useEffect, useState } from "react";
import API from "../api/api";
import { useNavigate } from "react-router-dom";

function Dashboard() {
  const [issues, setIssues] = useState([]);
  const navigate = useNavigate();

  // Fetch issues when page loads
  useEffect(() => {
    fetchIssues();
  }, []);

  const fetchIssues = async () => {
    try {
      const response = await API.get("/issues");
      setIssues(response.data);
    } catch (error) {
      console.error(error);
      alert("Failed to load issues");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Dashboard - Issues</h2>
        <button onClick={() => navigate("/create-issue")}>
            Create Issue
        </button>
        <button onClick={() => navigate("/chatbot")}>
            Open Chatbot
        </button>
        <button onClick={() => navigate("/study-planner")}>
            Study Planner
        </button>
      {issues.length === 0 ? (
        <p>No issues found</p>
      ) : (
        issues.map((issue) => (
          <div
            key={issue.id}
            style={{
              border: "1px solid #ccc",
              padding: "10px",
              marginBottom: "10px",
            }}
          >
            <h4>{issue.title}</h4>
            <p>{issue.description}</p>
            <p>Status: {issue.status}</p>
          </div>
        ))
      )}
    </div>
  );
}

export default Dashboard;