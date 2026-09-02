import MetarCard from "./MetarCard";
import TafCard from "./TafCard";

export default function StationGrid({ stations, loading, error }) {
  if (loading) return <div className="loading">Loading weather data...</div>;
  if (!stations.length) return null;

  return (
    <>
      {error && <div className="error">{error}</div>}
      <div className="dashboard-grid">
        {stations.map((s) =>
          s.metar || s.taf ? (
            <div key={s.station}>
              <MetarCard metar={s.metar} />
              <TafCard taf={s.taf} />
            </div>
          ) : (
            <div className="card" key={s.station}>
              <div className="card-title">{s.station}</div>
              <div className="field-value" style={{ color: "var(--text-muted)" }}>
                No current weather data
              </div>
            </div>
          )
        )}
      </div>
    </>
  );
}
