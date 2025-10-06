
import { useState } from "react";
import './App.css';

function App() {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const sendQuery = async () => {
    if (!query.trim()) {
      setAnswer("");
      setLoading(false);
      return;
    }
    setLoading(true);
    setAnswer("");
    try {
      const response = await fetch("https://ndaapi.dema.digital/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query }),
      });
      const data = await response.json();
      if (data.answer) {
        setAnswer(data.answer);
      } else {
        setAnswer(data.error || "Unknown error");
      }
    } catch (error) {
      setAnswer("Fetch error: " + error);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = async (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      sendQuery();
    }
  };

  return (
    
    <div className="app-center-container">
      <div className="nda-list-container">
      <h3>Known NDA Documents</h3>
      <ul className="nda-list">
        <li>AI Startups Ltd.</li>
        <li>Innovatech Inc.</li>
        <li>DataWorks GmbH</li>
        <li>NovaCorp</li>
        <li>Jane Williams</li>
        <li>Nino Gelashvili</li>
        <li>Oliver Brown</li>
        <li>Daniel Kaplan</li>
      </ul>
    </div>

      <div className="search-bar-wrapper">
        <input
          type="text"
          className="search-bar"
          placeholder="Example: Do we have an NDA with ..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        {query && (
          <button
            className="clear-btn"
            onClick={() => {
              setQuery("");
              setAnswer("");
            }}
            aria-label="Clear search"
          >
            &#10006;
          </button>
        )}
        <button
          className="send-btn"
          onClick={sendQuery}
          aria-label="Send query"
          disabled={loading || !query.trim()}
        >
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#007bff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
        </button>
      </div>
      {loading && (
        <div className="answer-box">
          <span>Thinking...</span>
        </div>
      )}
      {!loading && answer && (
        <div className="answer-box">
          {answer}
        </div>
      )}
    </div>
  );
}

export default App;