export default function TafCard({ taf }) {
  if (!taf) return null;

  return (
    <div className="card">
      <div className="card-header">
        <span className="card-title">TAF - {taf.station}</span>
        {taf.issue_time && (
          <span className="field-value" style={{ fontSize: 12, color: "var(--text-muted)" }}>
            Issued {taf.issue_time}
          </span>
        )}
      </div>
      {taf.forecast?.length > 0 && (
        <div className="forecast-list">
          {taf.forecast.map((f, i) => (
            <div key={i} className="forecast-item">
              {f.text}
            </div>
          ))}
        </div>
      )}
      {taf.raw && <div className="raw-text">{taf.raw}</div>}
    </div>
  );
}
