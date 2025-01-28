import { BrowserRouter, Routes, Route, Link, Navigate } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";
import { ScrollToTop } from "./components/ScrollToTop";
import "./components/AppHeader.css";
import Home from "./pages/Home";
import About from "./pages/About";
import Paper from "./pages/Paper";
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
          paddingTop: "3rem",
          padding: "3rem 2rem 2rem 2rem",
        }}
      >
        <nav
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            right: 0,
            padding: "0.35rem min(2rem, 4%)",
            backgroundColor: "white",
            // borderBottom: "1px solid #eaeaea",
            zIndex: 1000,
            // boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
          }}
        >
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              minHeight: "32px",
            }}
          >
            <Link
              to="/datasets"
              style={{
                display: "flex",
                alignItems: "center",
                textDecoration: "none",
                minWidth: 0,
                maxWidth: "calc(100% - 80px)",
              }}
            >
              <img
                src="/benchcompress/logo.svg"
                alt="Benchcompress Logo"
                style={{
                  width: "28px",
                  height: "28px",
                  marginRight: "10px",
                  flexShrink: 0,
                }}
              />
              <span
                style={{
                  minWidth: 0,
                  whiteSpace: "nowrap",
                  overflow: "hidden",
                  textOverflow: "ellipsis",
                }}
              >
                <span
                  style={{
                    fontSize: "1rem",
                    fontWeight: "500",
                    color: "#2c2c2c",
                  }}
                >
                  Benchcompress
                </span>
                <span className="app-header-subtitle">
                  {" · "}
                  <span style={{ fontSize: "1rem", color: "#777" }}>
                    Comparing compression algorithms for numeric time series
                    data
                  </span>
                </span>
              </span>
            </Link>
            <div style={{ display: "flex", gap: "1.5rem" }}>
              <Link
                to="/paper"
                style={{
                  color: "#0066cc",
                  textDecoration: "none",
                  fontWeight: "500",
                }}
              >
                Paper
              </Link>
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
              <Route path="/paper" element={<Paper />} />
            </Routes>
          )}
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
