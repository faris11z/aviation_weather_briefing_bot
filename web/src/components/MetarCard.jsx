export default function MetarCard({ metar }) {
  if (!metar) return null;

  return (
    <div className="card">
      <div className="card-header">
        <span className="card-title">METAR - {metar.station}</span>
        {metar.flight_category && (
          <span className={`flight-category ${metar.flight_category}`}>
            {metar.flight_category}
          </span>
        )}
      </div>
      <div className="field-grid">
        <div className="field">
          <span className="field-label">Time</span>
          <span className="field-value">{metar.time}</span>
        </div>
        <div className="field">
          <span className="field-label">Wind</span>
          <span className="field-value">{metar.wind}</span>
        </div>
        <div className="field">
          <span className="field-label">Visibility</span>
          <span className="field-value">{metar.visibility}</span>
        </div>
        <div className="field">
          <span className="field-label">Temp / Dew</span>
          <span className="field-value">
            {metar.temp}
            {metar.dewpoint ? ` / ${metar.dewpoint}` : ""}
          </span>
        </div>
        <div className="field">
          <span className="field-label">Altimeter</span>
          <span className="field-value">{metar.altimeter}</span>
        </div>
      </div>
      {metar.weather?.length > 0 && (
        <div style={{ marginTop: 12 }}>
          <span className="field-label">Weather</span>
          <div className="weather-list" style={{ marginTop: 4 }}>
            {metar.weather.map((w, i) => (
              <span key={i} className="tag">
                {w}
              </span>
            ))}
          </div>
        </div>
      )}
      {metar.clouds?.length > 0 && (
        <div style={{ marginTop: 12 }}>
          <span className="field-label">Clouds</span>
          <div className="clouds-list" style={{ marginTop: 4 }}>
            {metar.clouds.map((c, i) => (
              <span key={i} className="tag">
                {c}
              </span>
            ))}
          </div>
        </div>
      )}
      {metar.remarks && (
        <div style={{ marginTop: 12 }}>
          <span className="field-label">Remarks</span>
          <div className="field-value" style={{ marginTop: 4, fontSize: 12 }}>
            {metar.remarks}
          </div>
        </div>
      )}
      {metar.raw && <div className="raw-text">{metar.raw}</div>}
    </div>
  );
}
