import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Home from "./pages/Home";
import Datasets from "./pages/Datasets";
import Algorithms from "./pages/Algorithms";

function App() {
  return (
    <BrowserRouter>
      <div style={{ padding: "2rem" }}>
        <nav style={{ marginBottom: "2rem" }}>
          <ul style={{
            listStyle: "none",
            padding: 0,
            margin: 0,
            display: "flex",
            gap: "1.5rem"
          }}>
            <li>
              <Link
                to="/"
                style={{
                  color: "#0066cc",
                  textDecoration: "none",
                  fontWeight: "500"
                }}
              >
                Home
              </Link>
            </li>
            <li>
              <Link
                to="/datasets"
                style={{
                  color: "#0066cc",
                  textDecoration: "none",
                  fontWeight: "500"
                }}
              >
                Datasets
              </Link>
            </li>
            <li>
              <Link
                to="/algorithms"
                style={{
                  color: "#0066cc",
                  textDecoration: "none",
                  fontWeight: "500"
                }}
              >
                Algorithms
              </Link>
            </li>
          </ul>
        </nav>
        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/datasets" element={<Datasets />} />
            <Route path="/algorithms" element={<Algorithms />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
