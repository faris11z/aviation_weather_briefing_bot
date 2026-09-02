import MetarCard from "./MetarCard";
import TafCard from "./TafCard";

export default function StationGrid({ stations, loading, error }) {
  if (loading) return <div className="loading">Loading weather data...</div>;
  if (error) return <div className="error">{error}</div>;
  if (!stations.length) return null;

  return (
    <div className="dashboard-grid">
      {stations.map((s) => (
        <div key={s.station}>
          <MetarCard metar={s.metar} />
          <TafCard taf={s.taf} />
        </div>
      ))}
    </div>
  );
}
