import Plot from "react-plotly.js";
import { useState } from "react";

interface BenchmarkBarChartProps {
  title: string;
  data: ChartData[];
  dataKey: keyof Pick<
    ChartData,
    "compression_ratio" | "encode_speed" | "decode_speed"
  >;
  color: string;
  xAxisTitle: string;
}

function BenchmarkBarChart({
  title,
  data,
  dataKey,
  color,
  xAxisTitle,
}: BenchmarkBarChartProps) {
  return (
    <div style={{ margin: "0 20px 20px 0" }}>
      <h3 style={{ marginBottom: "10px" }}>{title}</h3>
      <Plot
        data={[
          {
            type: "bar",
            orientation: "h",
            y: data.map((d) => d.algorithm),
            x: data.map((d) => d[dataKey]),
            marker: { color },
          },
        ]}
        layout={{
          width: 700,
          height: Math.max(300, data.length * 23 + 40),
          margin: { t: 5, r: 30, l: 200, b: 30 },
          xaxis: { title: xAxisTitle },
          yaxis: { automargin: true, ticksuffix: "  " },
          dragmode: false,
        }}
        config={{ displayModeBar: false }}
      />
    </div>
  );
}

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
      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: "20px",
        }}
      >
        <BenchmarkBarChart
          title="Compression Ratio"
          data={sortedData}
          dataKey="compression_ratio"
          color="#8884d8"
          xAxisTitle="Ratio"
        />
        <BenchmarkBarChart
          title="Encode Speed (MB/s)"
          data={sortedData}
          dataKey="encode_speed"
          color="#82ca9d"
          xAxisTitle="MB/s"
        />
        <BenchmarkBarChart
          title="Decode Speed (MB/s)"
          data={sortedData}
          dataKey="decode_speed"
          color="#ff7300"
          xAxisTitle="MB/s"
        />
      </div>
    </div>
  );
}
