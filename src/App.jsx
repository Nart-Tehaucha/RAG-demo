import { useState } from "react";
import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const runQuery = async () => {
    if (!query.trim()) {
      setError("Please enter a query");
      return;
    }

    setLoading(true);
    setError(null);
    setResults([]);

    try {
      const response = await fetch(`http://localhost:5000/query?q=${encodeURIComponent(query)}`);
      
      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const data = await response.json();
      console.log("API Response:", data);
      setResults(data);
    } catch (err) {
      setError(`Failed to fetch results: ${err.message}`);
      console.error("Query error:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      runQuery();
    }
  };

  return (
    <div className="container">
      <div className="header">
        <h1>RAG Retrieval Demo</h1>
        <p>Trained on a tiny dataset for common IT helpdesk queries</p>
      </div>

      <div className="search-section">
        <div className="search-box">
          <input
            type="text"
            className="search-input"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Hint: Try asking about finding a lost PIN password..."
            disabled={loading}
          />
          <button 
            className="search-button"
            onClick={runQuery}
            disabled={loading}
          >
            {loading ? "Searching..." : "Search"}
          </button>
        </div>
      </div>

      {error && (
        <div className="error-message">
            {error}
        </div>
      )}

      <div className="results-section">
        {results.length === 0 && !loading && !error && (
          <div className="no-results">
            <p>No results yet. Try searching for something!</p>
          </div>
        )}

        {results.map((r, index) => (
          <div key={r.id || index} className="result-card">
            <div className="result-header">
              <span className="result-id">Chunk #{r.id}</span>
              <span className="result-similarity">
                Similarity: <strong>{(r.similarity * 100).toFixed(1)}%</strong>
              </span>
            </div>
            <p className="result-text">{r.text}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
