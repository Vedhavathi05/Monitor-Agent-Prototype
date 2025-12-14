import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [data, setData] = useState([]);
  const [status, setStatus] = useState("Stopped");

  const fetchData = async () => {
    const res = await fetch("http://127.0.0.1:8000/data");
    const json = await res.json();
    setData(json);
  };

  useEffect(() => {
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  const startMonitoring = async () => {
    await fetch("http://127.0.0.1:8000/start", { method: "POST" });
    setStatus("Monitoring...");
  };

  const stopMonitoring = async () => {
    await fetch("http://127.0.0.1:8000/stop", { method: "POST" });
    setStatus("Stopped");
  };

  return (
    <div className="page">
      {/* Header Card */}
      <div className="header-card">
        <h1>TV Monitor Agent</h1>

        <div className="controls">
          <button className="btn start" onClick={startMonitoring}>
            Start Monitoring
          </button>
          <button className="btn stop" onClick={stopMonitoring}>
            Stop Monitoring
          </button>
          <span className="status">
            Status: <strong>{status}</strong>
          </span>
        </div>
      </div>

      {/* Section Title */}
      <h2 className="section-title">
        Live Feed Transcripts & Summaries
      </h2>

      {/* Table */}
      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th className="col-time">Timestamp</th>
              <th className="col-transcript">Transcript</th>
              <th className="col-summary">AI Summary</th>
            </tr>
          </thead>
          <tbody>
            {data.map((item, index) => (
              <tr key={index}>
                <td className="timestamp">
                  {item.timestamp}
                  <br />
                  <span className="window">{item.video_window}</span>
                </td>
                <td className="transcript">{item.transcript}</td>
                <td className="summary">{item.summary}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;
