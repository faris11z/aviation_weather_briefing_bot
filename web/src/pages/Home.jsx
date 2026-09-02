import { useState } from "react";
import SearchBar from "../components/SearchBar";
import MetarCard from "../components/MetarCard";
import TafCard from "../components/TafCard";
import { fetchBrief } from "../api";

export default function Home() {
  const [station, setStation] = useState(null);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const search = async (icao) => {
    setStation(icao);
    setLoading(true);
    setError(null);
    setData(null);
    try {
      const res = await fetchBrief(icao);
      const first = res.stations?.[0] || null;
      if (first && (first.metar || first.taf)) {
        setData(first);
      } else {
        setError(`No weather data found for ${icao}`);
      }
    } catch (e) {
      setError(`Failed to fetch weather for ${icao}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="hero">
        <h1>Aviation Weather Briefing</h1>
        <p className="hero-desc">
          Real-time weather data for pilots, dispatchers, and aviation
          enthusiasts. Look up current conditions and forecasts for any airport
          worldwide.
        </p>
        <div className="hero-features">
          <span className="hero-tag">
            <strong>METAR</strong> Current conditions
          </span>
          <span className="hero-tag">
            <strong>TAF</strong> Forecasts
          </span>
          <span className="hero-tag">
            <strong>Dashboard</strong> Multi-airport monitor
          </span>
        </div>
      </div>
      <h2 style={{ fontSize: 20, marginBottom: 8 }}>Weather Lookup</h2>
      <p style={{ color: "var(--text-muted)", marginBottom: 20 }}>
        Enter an ICAO airport code (e.g. KLAX, KJFK, EGLL)
      </p>
      <SearchBar onSelect={search} />
      {loading && <div className="loading">Fetching weather for {station}...</div>}
      {error && <div className="error">{error}</div>}
      {data && (
        <>
          <MetarCard metar={data.metar} />
          <TafCard taf={data.taf} />
        </>
      )}
      {!data && !loading && !error && (
        <div className="empty">
          <h2>✈</h2>
          <p>Search for an airport to see weather data</p>
        </div>
      )}
    </div>
  );
}
