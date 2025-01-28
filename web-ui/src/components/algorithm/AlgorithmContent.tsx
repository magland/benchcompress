import { Algorithm, BenchmarkData } from "../../types";
import "./AlgorithmContent.css";
import { useNavigate } from "react-router-dom";
import { BenchmarkCharts } from "../benchmark/charts/BenchmarkCharts";
import { BenchmarkTable } from "../benchmark/table/BenchmarkTable";

type ChartData = Array<{
  algorithm: string;
  compression_ratio: number;
  encode_speed: number;
  decode_speed: number;
}>;

interface AlgorithmContentProps {
  algorithm: Algorithm;
  benchmarkData: BenchmarkData | null;
  chartData: ChartData;
}

export const AlgorithmContent = ({
  algorithm,
  benchmarkData,
  chartData,
}: AlgorithmContentProps) => {
  const navigate = useNavigate();

  return (
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
          <span style={{ fontSize: "0.9rem" }}>{algorithm.version}</span>
        </div>
        <div>
          <span style={{ fontWeight: "bold", fontSize: "0.9rem" }}>Tags: </span>
          {algorithm.tags.map((tag) => (
            <span
              onClick={() => navigate(`/algorithms?tag=${tag}`)}
              key={tag}
              className="algorithm-tag"
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
  );
};
