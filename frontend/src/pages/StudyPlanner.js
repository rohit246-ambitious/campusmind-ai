import React, { useState } from "react";
import API from "../api/api";

function StudyPlanner() {
  const [input, setInput] = useState("");
  const [plan, setPlan] = useState(null);

  const generatePlan = async () => {
    if (!input.trim()) return;

    try {
      const response = await API.post("/study-plan/generate", {
        message: input,
      });

      console.log("API Response:", response.data);

      setPlan(response.data.plan);

    } catch (error) {
      console.error(error);
      alert("Failed to generate study plan");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>AI Study Planner 📚</h2>

      {/* Input */}
      <input
        type="text"
        placeholder="e.g. I have exams in 5 days"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        style={{ width: "70%", padding: "8px" }}
      />

      <button onClick={generatePlan} style={{ marginLeft: "10px" }}>
        Generate
      </button>

      <br /><br />

      {/* Output */}
      {plan && (
        <div>
          <h3>Your Study Plan</h3>

          {/* ✅ CASE 1: If backend returns ARRAY */}
          {Array.isArray(plan) &&
            plan.map((item, index) => (
              <div
                key={index}
                style={{
                  border: "1px solid #ccc",
                  padding: "10px",
                  marginBottom: "10px",
                  borderRadius: "8px",
                }}
              >
                <strong>{item.day}</strong>
                <p>{item.task}</p>
              </div>
            ))}

          {/* ✅ CASE 2: If backend returns OBJECT */}
          {!Array.isArray(plan) &&
            Object.entries(plan).map(([day, task]) => (
              <div
                key={day}
                style={{
                  border: "1px solid #ccc",
                  padding: "10px",
                  marginBottom: "10px",
                  borderRadius: "8px",
                }}
              >
                <strong>{day.toUpperCase()}</strong>
                <p>{task}</p>
              </div>
            ))}
        </div>
      )}
    </div>
  );
}

export default StudyPlanner;