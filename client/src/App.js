import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [repositories, setRepositories] = useState([]);
  const [selectedRepo, setSelectedRepo] = useState("");

  useEffect(() => {
    // Fetch repositories from backend
    axios
      .get("http://localhost:5000/repositories", { withCredentials: true })
      .then((response) => setRepositories(response.data))
      .catch((error) => console.error("Error fetching repositories:", error));
  }, []);

  const handleLogin = () => {
    window.location.href = "http://localhost:5000/login";
  };

  const handleCreateWebhook = () => {
    axios
      .post(
        "http://localhost:5000/create-webhook",
        { repo: selectedRepo },
        { withCredentials: true }
      )
      .then((response) => console.log("Webhook created:", response.data))
      .catch((error) => console.error("Error creating webhook:", error));
  };

  return (
    <div className="App">
      <button onClick={handleLogin}>Login with GitHub</button>
      <ul>
        {repositories.map((repo) => (
          <li key={repo.id}>
            <input
              type="radio"
              value={repo.full_name}
              checked={selectedRepo === repo.full_name}
              onChange={() => setSelectedRepo(repo.full_name)}
            />
            {repo.name}
          </li>
        ))}
      </ul>
      <button onClick={handleCreateWebhook} disabled={!selectedRepo}>
        Create Webhook
      </button>
    </div>
  );
}

export default App;
