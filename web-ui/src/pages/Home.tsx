import { Link, useLocation, useParams } from "react-router-dom";
import { BenchmarkTable } from "../components/benchmark/table/BenchmarkTable";
import { useEffect, useRef, useState } from "react";
import TimeseriesView from "../components/dataset/TimeseriesView";
import { BenchmarkCharts } from "../components/benchmark/charts/BenchmarkCharts";
import { useBenchmarkChartData } from "../hooks/useBenchmarkChartData";
import { TagFilter } from "../components/TagFilter";
import { useTagFilter } from "../hooks/useTagFilter";
import { BenchmarkData } from "../types";

interface HomeProps {
  benchmarkData: BenchmarkData | null;
}

export default function Home({ benchmarkData }: HomeProps) {
  const location = useLocation();
  const { datasetName, algorithmName } = useParams<{
    datasetName?: string;
    algorithmName?: string;
  }>();
  const containerRef = useRef<HTMLDivElement>(null);
  const [containerWidth, setContainerWidth] = useState(1200);

  useEffect(() => {
    if (!containerRef.current) return;

    const resizeObserver = new ResizeObserver((entries) => {
      for (const entry of entries) {
        setContainerWidth(entry.contentRect.width - 32);
      }
    });

    resizeObserver.observe(containerRef.current);

    return () => {
      resizeObserver.disconnect();
    };
  }, []);

  // Determine active tab based on URL
  const getActiveTab = () => {
    if (datasetName) return `dataset-${datasetName}`;
    if (algorithmName) return `algorithm-${algorithmName}`;
    if (location.pathname.includes("/algorithms")) return "algorithms";
    return "datasets";
  };

  const activeTab = getActiveTab();

  // Get specific dataset or algorithm if viewing one
  const dataset = datasetName
    ? benchmarkData?.datasets.find((d) => d.name === datasetName)
    : undefined;
  const algorithm = algorithmName
    ? benchmarkData?.algorithms.find((a) => a.name === algorithmName)
    : undefined;

  // Get chart data for specific dataset or algorithm view
  const chartData = useBenchmarkChartData(
    benchmarkData?.results || [],
    dataset?.name || null,
    algorithm?.name || null,
  );

  // Set up tag filtering for datasets
  const {
    selectedTags: datasetTags,
    availableTags: availableDatasetTags,
    filteredItems: filteredDatasets,
    toggleTag: toggleDatasetTag,
  } = useTagFilter(benchmarkData?.datasets || []);

  // Set up tag filtering for algorithms
  const {
    selectedTags: algorithmTags,
    availableTags: availableAlgorithmTags,
    filteredItems: filteredAlgorithms,
    toggleTag: toggleAlgorithmTag,
  } = useTagFilter(benchmarkData?.algorithms || []);

  const renderDatasets = () => (
    <div style={{ overflowX: "auto" }}>
      <div style={{ marginBottom: "1rem" }}>
        <TagFilter
          availableTags={availableDatasetTags}
          selectedTags={datasetTags}
          onTagToggle={toggleDatasetTag}
          label="Filter datasets"
        />
      </div>
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ backgroundColor: "#f5f5f5" }}>
            <th
              style={{
                padding: "8px 12px",
                textAlign: "left",
                borderBottom: "1px solid #ddd",
                fontSize: "0.9rem",
                whiteSpace: "nowrap",
              }}
            >
              Name
            </th>
            <th
              style={{
                padding: "8px 12px",
                textAlign: "left",
                borderBottom: "1px solid #ddd",
                fontSize: "0.9rem",
                whiteSpace: "nowrap",
              }}
            >
              Version
            </th>
            <th
              style={{
                padding: "8px 12px",
                textAlign: "left",
                borderBottom: "1px solid #ddd",
                fontSize: "0.9rem",
                whiteSpace: "nowrap",
              }}
            >
              Description
            </th>
            <th
              style={{
                padding: "8px 12px",
                textAlign: "left",
                borderBottom: "1px solid #ddd",
                fontSize: "0.9rem",
                whiteSpace: "nowrap",
              }}
            >
              Tags
            </th>
            <th
              style={{
                padding: "8px 12px",
                textAlign: "left",
                borderBottom: "1px solid #ddd",
                fontSize: "0.9rem",
                whiteSpace: "nowrap",
              }}
            >
              Source
            </th>
            <th
              style={{
                padding: "8px 12px",
                textAlign: "left",
                borderBottom: "1px solid #ddd",
                fontSize: "0.9rem",
                whiteSpace: "nowrap",
              }}
            >
              Data
            </th>
          </tr>
        </thead>
        <tbody>
          {filteredDatasets.map((dataset, index) => (
            <tr
              key={`${dataset.name}-${dataset.version}`}
              style={{ backgroundColor: index % 2 === 0 ? "white" : "#fafafa" }}
            >
              <td
                style={{
                  padding: "6px 12px",
                  borderBottom: "1px solid #ddd",
                  fontSize: "0.9rem",
                }}
              >
                <Link
                  to={`/dataset/${encodeURIComponent(dataset.name)}`}
                  style={{
                    color: "#0066cc",
                    textDecoration: "none",
                    fontWeight: "500",
                  }}
                >
                  {dataset.name}
                </Link>
              </td>
              <td
                style={{
                  padding: "6px 12px",
                  borderBottom: "1px solid #ddd",
                  fontSize: "0.9rem",
                }}
              >
                {dataset.version}
              </td>
              <td
                style={{
                  padding: "6px 12px",
                  borderBottom: "1px solid #ddd",
                  fontSize: "0.9rem",
                }}
              >
                {dataset.description}
              </td>
              <td
                style={{
                  padding: "6px 12px",
                  borderBottom: "1px solid #ddd",
                  fontSize: "0.9rem",
                }}
              >
                {dataset.tags.map((tag) => (
                  <span
                    key={tag}
                    style={{
                      display: "inline-block",
                      backgroundColor: "#e1e1e1",
                      padding: "2px 6px",
                      borderRadius: "3px",
                      margin: "1px",
                      fontSize: "0.8rem",
                    }}
                  >
                    {tag}
                  </span>
                ))}
              </td>
              <td
                style={{
                  padding: "6px 12px",
                  borderBottom: "1px solid #ddd",
                  fontSize: "0.9rem",
                }}
              >
                {dataset.source_file && (
                  <a
                    href={dataset.source_file}
                    target="_blank"
                    rel="noopener noreferrer"
                    style={{ color: "#0066cc", textDecoration: "none" }}
                  >
                    View Source
                  </a>
                )}
              </td>
              <td
                style={{
                  padding: "6px 12px",
                  borderBottom: "1px solid #ddd",
                  fontSize: "0.9rem",
                }}
              >
                {dataset.data_url_npy && (
                  <a
                    href={dataset.data_url_npy}
                    download={`${dataset.name}-${dataset.version}.npy`}
                    style={{ color: "#0066cc", textDecoration: "none" }}
                  >
                    Download
                  </a>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );

  const renderAlgorithms = () => (
    <div style={{ overflowX: "auto" }}>
      <div style={{ marginBottom: "1rem" }}>
        <TagFilter
          availableTags={availableAlgorithmTags}
          selectedTags={algorithmTags}
          onTagToggle={toggleAlgorithmTag}
          label="Filter algorithms"
        />
      </div>
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ backgroundColor: "#f5f5f5" }}>
            <th
              style={{
                padding: "8px 12px",
                textAlign: "left",
                borderBottom: "1px solid #ddd",
                fontSize: "0.9rem",
                whiteSpace: "nowrap",
              }}
            >
              Name
            </th>
            <th
              style={{
                padding: "8px 12px",
                textAlign: "left",
                borderBottom: "1px solid #ddd",
                fontSize: "0.9rem",
                whiteSpace: "nowrap",
              }}
            >
              Version
            </th>
            <th
              style={{
                padding: "8px 12px",
                textAlign: "left",
                borderBottom: "1px solid #ddd",
                fontSize: "0.9rem",
                whiteSpace: "nowrap",
              }}
            >
              Description
            </th>
            <th
              style={{
                padding: "8px 12px",
                textAlign: "left",
                borderBottom: "1px solid #ddd",
                fontSize: "0.9rem",
                whiteSpace: "nowrap",
              }}
            >
              Tags
            </th>
            <th
              style={{
                padding: "8px 12px",
                textAlign: "left",
                borderBottom: "1px solid #ddd",
                fontSize: "0.9rem",
                whiteSpace: "nowrap",
              }}
            >
              Source
            </th>
          </tr>
        </thead>
        <tbody>
          {filteredAlgorithms.map((algorithm, index) => (
            <tr
              key={`${algorithm.name}-${algorithm.version}`}
              style={{ backgroundColor: index % 2 === 0 ? "white" : "#fafafa" }}
            >
              <td
                style={{
                  padding: "6px 12px",
                  borderBottom: "1px solid #ddd",
                  fontSize: "0.9rem",
                }}
              >
                <Link
                  to={`/algorithm/${encodeURIComponent(algorithm.name)}`}
                  style={{
                    color: "#0066cc",
                    textDecoration: "none",
                    fontWeight: "500",
                  }}
                >
                  {algorithm.name}
                </Link>
              </td>
              <td
                style={{
                  padding: "6px 12px",
                  borderBottom: "1px solid #ddd",
                  fontSize: "0.9rem",
                }}
              >
                {algorithm.version}
              </td>
              <td
                style={{
                  padding: "6px 12px",
                  borderBottom: "1px solid #ddd",
                  fontSize: "0.9rem",
                }}
              >
                {algorithm.description}
              </td>
              <td
                style={{
                  padding: "6px 12px",
                  borderBottom: "1px solid #ddd",
                  fontSize: "0.9rem",
                }}
              >
                {algorithm.tags.map((tag) => (
                  <span
                    key={tag}
                    style={{
                      display: "inline-block",
                      backgroundColor: "#e1e1e1",
                      padding: "2px 6px",
                      borderRadius: "3px",
                      margin: "1px",
                      fontSize: "0.8rem",
                    }}
                  >
                    {tag}
                  </span>
                ))}
              </td>
              <td
                style={{
                  padding: "6px 12px",
                  borderBottom: "1px solid #ddd",
                  fontSize: "0.9rem",
                }}
              >
                {algorithm.source_file && (
                  <a
                    href={algorithm.source_file}
                    target="_blank"
                    rel="noopener noreferrer"
                    style={{ color: "#0066cc", textDecoration: "none" }}
                  >
                    View Source
                  </a>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );

  return (
    <div>
      <header style={{ marginBottom: "2rem" }}>
        <h1 style={{ fontSize: "2rem", fontWeight: "bold", color: "#333" }}>
          Benchcompress
        </h1>
        <p style={{ color: "#666", marginTop: "0.5rem" }}>
          Comparing compression algorithms for numeric arrays
        </p>
      </header>
      <main>
        <div style={{ marginBottom: "1rem" }}>
          <div
            style={{
              borderBottom: "1px solid #ddd",
              display: "flex",
              gap: "4px",
              overflowX: "auto",
            }}
          >
            <Link
              to="/datasets"
              style={{
                padding: "8px 16px",
                border: "none",
                background: "none",
                borderBottom:
                  activeTab === "datasets" ? "2px solid #0066cc" : "none",
                color: activeTab === "datasets" ? "#0066cc" : "#666",
                fontWeight: activeTab === "datasets" ? "600" : "normal",
                cursor: "pointer",
                textDecoration: "none",
                whiteSpace: "nowrap",
              }}
            >
              Datasets
            </Link>
            <Link
              to="/algorithms"
              style={{
                padding: "8px 16px",
                border: "none",
                background: "none",
                borderBottom:
                  activeTab === "algorithms" ? "2px solid #0066cc" : "none",
                color: activeTab === "algorithms" ? "#0066cc" : "#666",
                fontWeight: activeTab === "algorithms" ? "600" : "normal",
                cursor: "pointer",
                textDecoration: "none",
                whiteSpace: "nowrap",
              }}
            >
              Algorithms
            </Link>
            {dataset && (
              <Link
                to={`/dataset/${dataset.name}`}
                style={{
                  padding: "8px 16px",
                  border: "none",
                  background: "none",
                  borderBottom:
                    activeTab === `dataset-${dataset.name}`
                      ? "2px solid #0066cc"
                      : "none",
                  color:
                    activeTab === `dataset-${dataset.name}`
                      ? "#0066cc"
                      : "#666",
                  fontWeight:
                    activeTab === `dataset-${dataset.name}` ? "600" : "normal",
                  cursor: "pointer",
                  textDecoration: "none",
                  whiteSpace: "nowrap",
                }}
              >
                {dataset.name}
              </Link>
            )}
            {algorithm && (
              <Link
                to={`/algorithm/${algorithm.name}`}
                style={{
                  padding: "8px 16px",
                  border: "none",
                  background: "none",
                  borderBottom:
                    activeTab === `algorithm-${algorithm.name}`
                      ? "2px solid #0066cc"
                      : "none",
                  color:
                    activeTab === `algorithm-${algorithm.name}`
                      ? "#0066cc"
                      : "#666",
                  fontWeight:
                    activeTab === `algorithm-${algorithm.name}`
                      ? "600"
                      : "normal",
                  cursor: "pointer",
                  textDecoration: "none",
                  whiteSpace: "nowrap",
                }}
              >
                {algorithm.name}
              </Link>
            )}
          </div>
        </div>

        <div style={{ padding: "1rem 0" }}>
          {dataset ? (
            <div>
              <div style={{ marginBottom: "1.5rem" }}>
                <p style={{ fontSize: "0.9rem", lineHeight: "1.5" }}>
                  {dataset.description}
                </p>
              </div>
              <div
                style={{
                  marginBottom: "1.5rem",
                  display: "flex",
                  gap: "2rem",
                  flexWrap: "wrap",
                }}
              >
                <div>
                  <span style={{ fontWeight: "bold", fontSize: "0.9rem" }}>
                    Version:{" "}
                  </span>
                  <span style={{ fontSize: "0.9rem" }}>{dataset.version}</span>
                </div>
                <div>
                  <span style={{ fontWeight: "bold", fontSize: "0.9rem" }}>
                    Tags:{" "}
                  </span>
                  {dataset.tags.map((tag) => (
                    <span
                      key={tag}
                      style={{
                        display: "inline-block",
                        backgroundColor: "#e1e1e1",
                        padding: "2px 6px",
                        borderRadius: "3px",
                        margin: "2px",
                        fontSize: "0.8rem",
                      }}
                    >
                      {tag}
                    </span>
                  ))}
                </div>
                <div>
                  <span style={{ fontWeight: "bold", fontSize: "0.9rem" }}>
                    Download:{" "}
                  </span>
                  <span style={{ display: "inline-flex", gap: "0.5rem" }}>
                    {dataset.data_url_npy && (
                      <a
                        href={dataset.data_url_npy}
                        download={`${dataset.name}-${dataset.version}.npy`}
                        style={{
                          color: "#0066cc",
                          textDecoration: "none",
                          padding: "2px 6px",
                          backgroundColor: "#f0f0f0",
                          borderRadius: "4px",
                          fontSize: "0.9rem",
                        }}
                      >
                        NPY
                      </a>
                    )}
                    {dataset.data_url_raw && (
                      <a
                        href={dataset.data_url_raw}
                        download={`${dataset.name}-${dataset.version}.dat`}
                        style={{
                          color: "#0066cc",
                          textDecoration: "none",
                          padding: "2px 6px",
                          backgroundColor: "#f0f0f0",
                          borderRadius: "4px",
                          fontSize: "0.9rem",
                        }}
                      >
                        RAW
                      </a>
                    )}
                  </span>
                </div>
                {dataset.source_file && (
                  <div>
                    <span style={{ fontWeight: "bold", fontSize: "0.9rem" }}>
                      Source:{" "}
                    </span>
                    <a
                      href={dataset.source_file}
                      target="_blank"
                      rel="noopener noreferrer"
                      style={{
                        color: "#0066cc",
                        textDecoration: "none",
                        padding: "2px 6px",
                        backgroundColor: "#f0f0f0",
                        borderRadius: "4px",
                        fontSize: "0.9rem",
                      }}
                    >
                      View
                    </a>
                  </div>
                )}
              </div>
              <div style={{ marginBottom: "1.5rem" }}>
                <div
                  ref={containerRef}
                  style={{
                    width: "100%",
                    height: "300px",
                    backgroundColor: "#f5f5f5",
                    borderRadius: "4px",
                    padding: "1rem",
                  }}
                >
                  <TimeseriesView
                    width={containerWidth}
                    height={250}
                    dataset={dataset}
                  />
                </div>
              </div>
              {benchmarkData && (
                <>
                  <div style={{ marginBottom: "1.5rem" }}>
                    <h2
                      style={{
                        fontSize: "1.2rem",
                        fontWeight: "bold",
                        marginBottom: "0.5rem",
                      }}
                    >
                      Benchmark Results
                    </h2>
                    <BenchmarkCharts chartData={chartData} />
                  </div>
                  <div style={{ marginBottom: "1.5rem" }}>
                    <BenchmarkTable
                      results={benchmarkData.results.filter(
                        (result) => result.dataset === dataset.name,
                      )}
                    />
                  </div>
                </>
              )}
            </div>
          ) : algorithm ? (
            <div>
              <div style={{ marginBottom: "1.5rem" }}>
                <p style={{ fontSize: "0.9rem", lineHeight: "1.5" }}>
                  {algorithm.description}
                </p>
              </div>
              <div
                style={{
                  marginBottom: "1.5rem",
                  display: "flex",
                  gap: "2rem",
                  flexWrap: "wrap",
                }}
              >
                <div>
                  <span style={{ fontWeight: "bold", fontSize: "0.9rem" }}>
                    Version:{" "}
                  </span>
                  <span style={{ fontSize: "0.9rem" }}>
                    {algorithm.version}
                  </span>
                </div>
                <div>
                  <span style={{ fontWeight: "bold", fontSize: "0.9rem" }}>
                    Tags:{" "}
                  </span>
                  {algorithm.tags.map((tag) => (
                    <span
                      key={tag}
                      style={{
                        display: "inline-block",
                        backgroundColor: "#e1e1e1",
                        padding: "2px 6px",
                        borderRadius: "3px",
                        margin: "2px",
                        fontSize: "0.8rem",
                      }}
                    >
                      {tag}
                    </span>
                  ))}
                </div>
                {algorithm.source_file && (
                  <div>
                    <span style={{ fontWeight: "bold", fontSize: "0.9rem" }}>
                      Source:{" "}
                    </span>
                    <a
                      href={algorithm.source_file}
                      target="_blank"
                      rel="noopener noreferrer"
                      style={{
                        color: "#0066cc",
                        textDecoration: "none",
                        padding: "2px 6px",
                        backgroundColor: "#f0f0f0",
                        borderRadius: "4px",
                        fontSize: "0.9rem",
                      }}
                    >
                      View
                    </a>
                  </div>
                )}
              </div>
              {benchmarkData && (
                <>
                  <div style={{ marginBottom: "1.5rem" }}>
                    <h2
                      style={{
                        fontSize: "1.2rem",
                        fontWeight: "bold",
                        marginBottom: "0.5rem",
                      }}
                    >
                      Benchmark Results
                    </h2>
                    <BenchmarkCharts chartData={chartData} />
                  </div>
                  <div style={{ marginBottom: "1.5rem" }}>
                    <BenchmarkTable
                      results={benchmarkData.results.filter(
                        (result) => result.algorithm === algorithm.name,
                      )}
                    />
                  </div>
                </>
              )}
            </div>
          ) : activeTab === "datasets" ? (
            renderDatasets()
          ) : (
            renderAlgorithms()
          )}
        </div>
      </main>
    </div>
  );
}
