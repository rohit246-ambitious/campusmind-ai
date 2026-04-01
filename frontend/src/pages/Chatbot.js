import React, { useState } from "react";
import API from "../api/api";

function Chatbot() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);

  const sendMessage = async () => {
    if (!message.trim()) return;

    // Add user message to chat
    const newChat = [...chat, { sender: "user", text: message }];
    setChat(newChat);

    try {
      const response = await API.post("/chatbot/ask", {
        message: message,
      });

      // Add bot response
      setChat([
        ...newChat,
        { sender: "bot", text: response.data.reply },
      ]);

    } catch (error) {
      setChat([
        ...newChat,
        { sender: "bot", text: "Error fetching response" },
      ]);
    }

    setMessage("");
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Campus Chatbot 🤖</h2>

      {/* Chat Box */}
      <div
        style={{
          border: "1px solid #ccc",
          height: "400px",
          overflowY: "scroll",
          padding: "10px",
          marginBottom: "10px",
        }}
      >
        {chat.map((msg, index) => (
          <div key={index}>
            <strong>{msg.sender}:</strong> {msg.text}
          </div>
        ))}
      </div>

      {/* Input */}
      <input
        type="text"
        placeholder="Ask something..."
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        style={{ width: "70%" }}
      />

      <button onClick={sendMessage}>Send</button>
    </div>
  );
}

export default Chatbot;