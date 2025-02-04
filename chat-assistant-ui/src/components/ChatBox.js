import React, { useState } from 'react';
import axios from 'axios';

const ChatBox = () => {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post('http://127.0.0.1:5000/chat', { query });
      setResponse(res.data.response);
    } catch {
      setResponse('Error: Unable to fetch response.');
    }
  };

  return (
    <div className="bg-white shadow-xl p-6 rounded-lg max-w-md mx-auto mt-10">
      <h2 className="text-2xl font-semibold text-center mb-4">💬 Chat Assistant</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="text"
          placeholder="Ask something..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
        <button
          type="submit"
          className="w-full bg-blue-500 text-white py-2 rounded-md hover:bg-blue-600 transition"
        >
          Send
        </button>
      </form>
      {response && (
        <div className="mt-4 p-4 bg-gray-100 rounded-md shadow-sm">
          <strong>Response:</strong> {response}
        </div>
      )}
    </div>
  );
};

export default ChatBox;
