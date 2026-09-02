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
      <h1 style={{ fontSize: 24, marginBottom: 8 }}>Weather Lookup</h1>
      <p style={{ color: "var(--text-muted)", marginBottom: 20 }}>
        Enter an ICAO airport code to get current METAR and TAF
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
