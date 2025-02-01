import React, { useState } from "react";
import axios from "axios";
import Home from "./components/Home";

function App() {
  const [searchTerm, setSearchTerm] = useState("");
  const [searchResults, setSearchResults] = useState([]);

  const handleSearch = async () => {
    if (!searchTerm.trim()) return;
    
    try {
      const response = await axios.get(`http://127.0.0.1:8000/search_song/?query=`+searchTerm);

      setSearchResults(response.data);
    } catch (error) {
      console.error("Error fetching search results:", error);
    }
  };

  return (
    <div className="container mt-4">
      <h1 className="text-center">YouTube Music Downloader</h1>
      
      {/* Search Input */}
      <div className="input-group mb-3">
        <input
          type="text"
          className="form-control"
          placeholder="Enter song name..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <button className="btn btn-primary" onClick={handleSearch}>
          Search
        </button>
      </div>

      {/* Results Section */}
      {searchResults.length > 0 && <Home newData={searchResults} />}
    </div>
  );
}

export default App;
