import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";
import Home from "./pages/Home";
import Datasets from "./pages/Datasets";
import Algorithms from "./pages/Algorithms";
import { BenchmarkData } from "./types";

function App() {
  const [benchmarkData, setBenchmarkData] = useState<BenchmarkData | null>(
    null,
  );
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsLoading(true);
        setError(null);
        const response = await axios.get(
          "https://raw.githubusercontent.com/magland/zia/benchmark-results/benchmark_results/results.json",
        );
        setBenchmarkData(response.data);
      } catch (error) {
        const message =
          error instanceof Error ? error.message : "Failed to fetch data";
        setError(message);
        console.error("Error fetching benchmark data:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  return (
    <BrowserRouter basename="/zia">
      <div style={{ padding: "2rem" }}>
        <nav style={{ marginBottom: "2rem" }}>
          <ul
            style={{
              listStyle: "none",
              padding: 0,
              margin: 0,
              display: "flex",
              gap: "1.5rem",
            }}
          >
            <li>
              <Link
                to="/home"
                style={{
                  color: "#0066cc",
                  textDecoration: "none",
                  fontWeight: "500",
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
                  fontWeight: "500",
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
                  fontWeight: "500",
                }}
              >
                Algorithms
              </Link>
            </li>
          </ul>
        </nav>
        <main>
          {isLoading ? (
            <div>Loading benchmark data...</div>
          ) : error ? (
            <div>Error: {error}</div>
          ) : (
            <Routes>
              <Route
                path="/home"
                element={<Home benchmarkData={benchmarkData} />}
              />
              <Route
                path="/"
                element={<Home benchmarkData={benchmarkData} />}
              />
              <Route
                path="/datasets"
                element={<Datasets datasets={benchmarkData?.datasets || []} />}
              />
              <Route
                path="/algorithms"
                element={
                  <Algorithms algorithms={benchmarkData?.algorithms || []} />
                }
              />
            </Routes>
          )}
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
