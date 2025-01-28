import { BrowserRouter, Routes, Route, Link, Navigate } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";
import { ScrollToTop } from "./components/ScrollToTop";
import Home from "./pages/Home";
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
          "https://raw.githubusercontent.com/magland/benchcompress/benchmark-results/benchmark_results/results.json",
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
    <BrowserRouter basename="/benchcompress">
      <ScrollToTop />
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
          <div style={{ display: "flex", justifyContent: "flex-end" }}>
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
          </div>
        </nav>
        <main>
          {isLoading ? (
            <div>Loading benchmark data...</div>
          ) : error ? (
            <div>Error: {error}</div>
          ) : (
            <Routes>
              <Route path="/" element={<Navigate to="/datasets" replace />} />
              <Route
                path="/datasets"
                element={<Home benchmarkData={benchmarkData} />}
              />
              <Route
                path="/algorithms"
                element={<Home benchmarkData={benchmarkData} />}
              />
              <Route
                path="/dataset/:datasetName"
                element={<Home benchmarkData={benchmarkData} />}
              />
              <Route
                path="/algorithm/:algorithmName"
                element={<Home benchmarkData={benchmarkData} />}
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
