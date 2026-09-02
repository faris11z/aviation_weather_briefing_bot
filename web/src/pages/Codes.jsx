import { useMemo, useState } from "react";
import { airports } from "../data/airports";

export default function Codes() {
  const [query, setQuery] = useState("");
  const [region, setRegion] = useState("All");

  const regions = useMemo(() => {
    const set = new Set(airports.map((a) => a.country));
    return ["All", ...Array.from(set).sort()];
  }, []);

  const filtered = useMemo(() => {
    const q = query.trim().toUpperCase();
    return airports.filter((a) => {
      const matchRegion = region === "All" || a.country === region;
      if (!matchRegion) return false;
      if (!q) return true;
      return (
        a.code.includes(q) ||
        a.name.toUpperCase().includes(q) ||
        a.city.toUpperCase().includes(q) ||
        a.iata.toUpperCase().includes(q)
      );
    });
  }, [query, region]);

  return (
    <div>
      <h1 style={{ fontSize: 24, marginBottom: 8 }}>Airport Codes</h1>
      <p style={{ color: "var(--text-muted)", marginBottom: 20 }}>
        Browse major airports worldwide and see their full form and codes.
        Filter by ICAO code, name, city, or IATA code.
      </p>

      <div className="add-station" style={{ alignItems: "center" }}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Filter by code, name, city, or IATA..."
        />
        <select
          value={region}
          onChange={(e) => setRegion(e.target.value)}
          style={{
            padding: "10px 12px",
            background: "var(--surface)",
            border: "1px solid var(--border)",
            borderRadius: 8,
            color: "var(--text)",
            fontSize: 14,
          }}
        >
          {regions.map((r) => (
            <option key={r} value={r}>
              {r}
            </option>
          ))}
        </select>
      </div>

      <p style={{ color: "var(--text-muted)", fontSize: 13, marginBottom: 16 }}>
        {filtered.length} of {airports.length} airports
      </p>

      {filtered.length === 0 && (
        <div className="empty">
          <h2>✈</h2>
          <p>No airports match your filter.</p>
        </div>
      )}

      <div className="dashboard-grid">
        {filtered.map((a) => (
          <div className="card" key={a.code} style={{ marginBottom: 12 }}>
            <div className="card-header">
              <span className="card-title">{a.code}</span>
              <span className="tag">{a.iata || "-"}</span>
            </div>
            <div style={{ fontWeight: 600, marginBottom: 4 }}>{a.name}</div>
            <div style={{ color: "var(--text-muted)", fontSize: 13 }}>
              {a.city}, {a.country}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
