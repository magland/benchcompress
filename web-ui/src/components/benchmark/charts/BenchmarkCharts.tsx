import Plot from "react-plotly.js";
import { useState } from "react";

interface ChartData {
  algorithm: string;
  compression_ratio: number;
  encode_speed: number;
  decode_speed: number;
}

interface BenchmarkChartsProps {
  chartData: ChartData[];
}

export function BenchmarkCharts({ chartData }: BenchmarkChartsProps) {
  const [sortByRatio, setSortByRatio] = useState(true);

  if (!chartData.length) return null;

  const sortedData = sortByRatio
    ? [...chartData].sort((a, b) => a.compression_ratio - b.compression_ratio)
    : chartData;

  return (
    <div>
      <div style={{ marginBottom: "10px" }}>
        <label style={{ display: "flex", alignItems: "center", gap: "8px" }}>
          <input
            type="checkbox"
            checked={sortByRatio}
            onChange={(e) => setSortByRatio(e.target.checked)}
          />
          Sort by compression ratio
        </label>
      </div>
      <div style={{ marginBottom: "30px" }}>
        <div style={{ marginBottom: "20px" }}>
          <h3 style={{ marginBottom: "10px" }}>Compression Ratio</h3>
          <Plot
            data={[
              {
                type: "bar",
                orientation: "h",
                y: sortedData.map((d) => d.algorithm),
                x: sortedData.map((d) => d.compression_ratio),
                marker: { color: "#8884d8" },
              },
            ]}
            layout={{
              width: 800,
              height: 400,
              margin: { t: 5, r: 30, l: 250, b: 30 },
              xaxis: { title: "Ratio" },
              dragmode: false,
            }}
            config={{ displayModeBar: false }}
          />
        </div>

        <div style={{ marginBottom: "20px" }}>
          <h3 style={{ marginBottom: "10px" }}>Encode Speed (MB/s)</h3>
          <Plot
            data={[
              {
                type: "bar",
                orientation: "h",
                y: sortedData.map((d) => d.algorithm),
                x: sortedData.map((d) => d.encode_speed),
                marker: { color: "#82ca9d" },
              },
            ]}
            layout={{
              width: 800,
              height: 400,
              margin: { t: 5, r: 30, l: 250, b: 30 },
              xaxis: { title: "MB/s" },
            }}
            config={{ displayModeBar: false }}
          />
        </div>

        <div style={{ marginBottom: "20px" }}>
          <h3 style={{ marginBottom: "10px" }}>Decode Speed (MB/s)</h3>
          <Plot
            data={[
              {
                type: "bar",
                orientation: "h",
                y: sortedData.map((d) => d.algorithm),
                x: sortedData.map((d) => d.decode_speed),
                marker: { color: "#ff7300" },
              },
            ]}
            layout={{
              width: 800,
              height: 400,
              margin: { t: 5, r: 30, l: 250, b: 30 },
              xaxis: { title: "MB/s" },
            }}
            config={{ displayModeBar: false }}
          />
        </div>
      </div>
    </div>
  );
}
