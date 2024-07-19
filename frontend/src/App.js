import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [question, setQuestion] = useState('');
  const [uploads, setUploads] = useState([]);

  useEffect(() => {
    fetchUploads();
  }, []);

  const fetchUploads = async () => {
    try {
      const response = await fetch('http://localhost:5000/uploads');
      const data = await response.json();
      console.log('Fetched uploads:', data);
      setUploads(data);
    } catch (error) {
      console.error('Error fetching uploads:', error);
    }
  };

  const handleQuestionChange = (event) => {
    setQuestion(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    const formData = { question };

    try {
      const response = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const result = await response.json();
      console.log('Upload result:', result);
      setUploads([...uploads, result]);
      setQuestion('');
    } catch (error) {
      console.error('Error uploading:', error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Ask a Question About Music</h1>
        <form onSubmit={handleSubmit}>
          <div>
            <label>
              Question:
              <input type="text" value={question} onChange={handleQuestionChange} />
            </label>
          </div>
          <button type="submit">Submit</button>
        </form>

        <h2>Uploaded Questions</h2>
        <ul>
          {uploads.map((upload, index) => (
            <li key={index}>
              <p>Question: {upload.question}</p>
              <p>Processed Data: {upload.processedData}</p>
            </li>
          ))}
        </ul>
      </header>
    </div>
  );
}

export default App;

