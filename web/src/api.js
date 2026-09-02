const API_BASE = import.meta.env.VITE_API_URL || "/api";

export async function fetchBrief(station, hours = 12) {
  const r = await fetch(
    `${API_BASE}/weather/brief?station=${encodeURIComponent(station)}&hours=${hours}`
  );
  if (!r.ok) throw new Error(`API error: ${r.status}`);
  return r.json();
}

export async function fetchMetar(station, hours = 3) {
  const r = await fetch(
    `${API_BASE}/weather/metar?station=${encodeURIComponent(station)}&hours=${hours}`
  );
  if (!r.ok) throw new Error(`API error: ${r.status}`);
  return r.json();
}

export async function fetchTaf(station, hours = 24) {
  const r = await fetch(
    `${API_BASE}/weather/taf?station=${encodeURIComponent(station)}&hours=${hours}`
  );
  if (!r.ok) throw new Error(`API error: ${r.status}`);
  return r.json();
}

export async function searchAirports(query) {
  const r = await fetch(
    `${API_BASE}/airports/search?q=${encodeURIComponent(query)}&limit=5`
  );
  if (!r.ok) throw new Error(`API error: ${r.status}`);
  return r.json();
}

export async function fetchAirportInfo(codes) {
  const r = await fetch(
    `${API_BASE}/airports/info?codes=${encodeURIComponent(codes)}`
  );
  if (!r.ok) throw new Error(`API error: ${r.status}`);
  return r.json();
}
