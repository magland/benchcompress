import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";
import Home from "./pages/Home";
import Datasets from "./pages/Datasets";
import Dataset from "./pages/Dataset";
import Algorithms from "./pages/Algorithms";
import About from "./pages/About";
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
      <div
        style={{
          paddingTop: "5rem",
          paddingLeft: "2rem",
          paddingRight: "2rem",
          paddingBottom: "2rem",
        }}
      >
        <nav
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            right: 0,
            padding: "1rem 2rem",
            backgroundColor: "white",
            borderBottom: "1px solid #eaeaea",
            zIndex: 1000,
            boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
          }}
        >
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
            <li>
              <Link
                to="/about"
                style={{
                  color: "#0066cc",
                  textDecoration: "none",
                  fontWeight: "500",
                }}
              >
                About
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
              <Route
                path="/dataset/:datasetName"
                element={<Dataset datasets={benchmarkData?.datasets || []} />}
              />
              <Route path="/about" element={<About />} />
            </Routes>
          )}
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
