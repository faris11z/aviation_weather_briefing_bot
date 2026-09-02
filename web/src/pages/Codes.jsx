import { useState } from "react";
import { fetchAirportInfo } from "../api";

function CodeCard({ info }) {
  return (
    <div className="card">
      <div className="card-header">
        <span className="card-title">{info.icao || info.name}</span>
        {info.name !== "Not found" && info.name && (
          <span className="tag">{info.name}</span>
        )}
      </div>
      <div className="field-grid">
        <div className="field">
          <span className="field-label">Full Name</span>
          <span className="field-value">{info.name}</span>
        </div>
        <div className="field">
          <span className="field-label">IATA</span>
          <span className="field-value">{info.iata || "-"}</span>
        </div>
        <div className="field">
          <span className="field-label">FAA</span>
          <span className="field-value">{info.faa || "-"}</span>
        </div>
        <div className="field">
          <span className="field-label">WMO</span>
          <span className="field-value">{info.wmo || "-"}</span>
        </div>
        <div className="field">
          <span className="field-label">Country</span>
          <span className="field-value">{info.country || "-"}</span>
        </div>
        <div className="field">
          <span className="field-label">State</span>
          <span className="field-value">{info.state || "-"}</span>
        </div>
        <div className="field">
          <span className="field-label">Latitude</span>
          <span className="field-value">{info.lat}</span>
        </div>
        <div className="field">
          <span className="field-label">Longitude</span>
          <span className="field-value">{info.lon}</span>
        </div>
      </div>
    </div>
  );
}

export default function Codes() {
  const [input, setInput] = useState("");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const submit = async (e) => {
    e.preventDefault();
    const trimmed = input.trim();
    if (!trimmed) return;
    setLoading(true);
    setError(null);
    setData(null);
    try {
      setData(await fetchAirportInfo(trimmed));
    } catch (err) {
      setError("Failed to fetch airport codes");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1 style={{ fontSize: 24, marginBottom: 8 }}>Airport Codes</h1>
      <p style={{ color: "var(--text-muted)", marginBottom: 20 }}>
        Look up the full name and alternate codes for any airport worldwide.
        Enter ICAO codes, comma or space separated (e.g. KLAX, EGLL).
      </p>

      <form className="add-station" onSubmit={submit}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Enter codes, e.g. KLAX, EGLL, RJTT"
        />
        <button type="submit">Lookup</button>
      </form>

      {loading && <div className="loading">Looking up airport codes...</div>}
      {error && <div className="error">{error}</div>}
      {data && (
        <div className="dashboard-grid">
          {data.map((info) => (
            <CodeCard key={info.icao} info={info} />
          ))}
        </div>
      )}
    </div>
  );
}
