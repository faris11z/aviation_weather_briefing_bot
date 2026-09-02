import { Routes, Route, Link } from "react-router-dom";
import Home from "./pages/Home";
import Dashboard from "./pages/Dashboard";
import Codes from "./pages/Codes";

export default function App() {
  return (
    <div className="app">
      <header className="header">
        <Link to="/" className="logo">
          ✈ Aviation Weather
        </Link>
        <nav>
          <Link to="/home">Home</Link>
          <Link to="/dashboard">Dashboard</Link>
          <Link to="/codes">Airport Codes</Link>
        </nav>
      </header>
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/home" element={<Home />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/codes" element={<Codes />} />
        </Routes>
      </main>
    </div>
  );
}
