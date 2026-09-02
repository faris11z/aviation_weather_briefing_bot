import { useState, useEffect, useCallback } from "react";
import StationGrid from "../components/StationGrid";
import { fetchBrief } from "../api";

const STORAGE_KEY = "wx_dashboard_stations";

function loadStations() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY)) || ["KLAX", "KJFK", "KORD"];
  } catch {
    return ["KLAX", "KJFK", "KORD"];
  }
}

function saveStations(stations) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(stations));
}

export default function Dashboard() {
  const [stations, setStations] = useState(loadStations);
  const [input, setInput] = useState("");
  const [data, setData] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const refresh = useCallback(async () => {
    if (!stations.length) return;
    setLoading(true);
    setError(null);
    try {
      const codes = stations.join(",");
      const res = await fetchBrief(codes);
      const map = {};
      for (const s of res.stations || []) map[s.station] = s;
      setData(map);
    } catch (e) {
      setError("Could not refresh weather data. Check your connection.");
    } finally {
      setLoading(false);
    }
  }, [stations]);

  useEffect(() => {
    refresh();
  }, [refresh]);

  useEffect(() => {
    const id = setInterval(refresh, 300000);
    return () => clearInterval(id);
  }, [refresh]);

  const addStation = (e) => {
    e.preventDefault();
    const code = input.trim().toUpperCase();
    if (code && !stations.includes(code)) {
      const next = [...stations, code];
      setStations(next);
      saveStations(next);
    }
    setInput("");
  };

  const removeStation = (code) => {
    const next = stations.filter((s) => s !== code);
    setStations(next);
    saveStations(next);
  };

  return (
    <div>
      <h1 style={{ fontSize: 24, marginBottom: 8 }}>Dashboard</h1>
      <p style={{ color: "var(--text-muted)", marginBottom: 20 }}>
        Monitor multiple airports at once. Auto-refreshes every 5 minutes.
      </p>

      <form className="add-station" onSubmit={addStation}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Add ICAO code..."
        />
        <button type="submit">Add</button>
      </form>

      <div className="station-chips">
        {stations.map((s) => (
          <span key={s} className="station-chip">
            {s}
            <button onClick={() => removeStation(s)}>&times;</button>
          </span>
        ))}
      </div>

      <StationGrid
        stations={stations.map((s) => data[s] || { station: s, metar: null, taf: null })}
        loading={loading}
        error={error}
      />
    </div>
  );
}
