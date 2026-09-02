import { useState, useEffect, useRef } from "react";
import { searchAirports } from "../api";

export default function SearchBar({ onSelect }) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [open, setOpen] = useState(false);
  const ref = useRef(null);

  useEffect(() => {
    if (query.length < 2) {
      setResults([]);
      return;
    }
    const t = setTimeout(() => {
      setLoading(true);
      searchAirports(query)
        .then(setResults)
        .catch(() => setResults([]))
        .finally(() => setLoading(false));
    }, 300);
    return () => clearTimeout(t);
  }, [query]);

  useEffect(() => {
    const handler = (e) => {
      if (ref.current && !ref.current.contains(e.target)) setOpen(false);
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, []);

  const pick = (icao) => {
    setQuery(icao);
    setOpen(false);
    onSelect(icao);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) onSelect(query.trim().toUpperCase());
  };

  return (
    <div className="search-container" ref={ref} style={{ position: "relative" }}>
      <form onSubmit={handleSubmit} style={{ display: "flex", flex: 1, gap: 8 }}>
        <input
          type="text"
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            setOpen(true);
          }}
          placeholder="Enter ICAO code (e.g. KLAX, EGLL)"
          style={{ flex: 1 }}
        />
        <button type="submit">Search</button>
      </form>
      {open && results.length > 0 && (
        <div
          style={{
            position: "absolute",
            top: "100%",
            left: 0,
            right: 80,
            background: "var(--surface)",
            border: "1px solid var(--border)",
            borderRadius: 8,
            zIndex: 10,
            maxHeight: 200,
            overflow: "auto",
          }}
        >
          {results.map((r) => (
            <div
              key={r.icao}
              onClick={() => pick(r.icao)}
              style={{
                padding: "10px 14px",
                cursor: "pointer",
                borderBottom: "1px solid var(--border)",
              }}
              onMouseEnter={(e) =>
                (e.target.style.background = "rgba(88,166,255,0.1)")
              }
              onMouseLeave={(e) => (e.target.style.background = "transparent")}
            >
              <strong>{r.icao}</strong>{" "}
              <span style={{ color: "var(--text-muted)", fontSize: 13 }}>
                {r.name}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
