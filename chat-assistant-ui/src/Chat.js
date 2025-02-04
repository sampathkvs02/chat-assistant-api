import React, { useState } from "react";
import axios from "axios";

const Chat = () => {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query) return;
    
    try {
      const res = await axios.post("http://127.0.0.1:5000/chat", { query });
      setResponse(res.data.response);
    } catch (error) {
      setResponse("Error: Unable to fetch response.");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-100">
      <h1 className="text-3xl font-bold mb-6">Chat Assistant</h1>
      <form onSubmit={handleSubmit} className="bg-white p-6 rounded shadow-lg w-96">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask a question..."
          className="w-full p-2 border rounded mb-4"
        />
        <button
          type="submit"
          className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600"
        >
          Ask
        </button>
      </form>
      {response && (
        <div className="mt-4 bg-gray-200 p-4 rounded w-96">
          <strong>Response:</strong> {response}
        </div>
      )}
    </div>
  );
};

export default Chat;