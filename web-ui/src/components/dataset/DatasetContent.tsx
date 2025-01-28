import { Dataset, BenchmarkData } from "../../types";
import TimeseriesView from "./TimeseriesView";
import { BenchmarkCharts } from "../benchmark/charts/BenchmarkCharts";
import { BenchmarkTable } from "../benchmark/table/BenchmarkTable";
import { useEffect, useRef, useState } from "react";
type ChartData = Array<{
  algorithm: string;
  compression_ratio: number;
  encode_speed: number;
  decode_speed: number;
}>;

interface DatasetContentProps {
  dataset: Dataset;
  benchmarkData: BenchmarkData | null;
  chartData: ChartData;
}

export const DatasetContent = ({
  dataset,
  benchmarkData,
  chartData,
}: DatasetContentProps) => {
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

  return (
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
          <span style={{ fontWeight: "bold", fontSize: "0.9rem" }}>Tags: </span>
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
  );
};
