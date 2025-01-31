import { useState } from "react";
import Plot from "react-plotly.js";

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
            y: data.map((d) => d.algorithmOrDataset),
            x: data.map((d) => d[dataKey]),
            marker: { color },
            name: title,
          },
          ...(dataKey === "compression_ratio" &&
          data.some((d) => d.reference_compression_ratio !== null)
            ? [
                ...data
                  .filter((d) => d.reference_compression_ratio !== null)
                  .flatMap((d) => [
                    {
                      type: "scatter" as const,
                      mode: "lines" as const,
                      y: [d.algorithmOrDataset, d.algorithmOrDataset],
                      x: [0, d.reference_compression_ratio],
                      line: { color: "#aaaaaa", width: 1 },
                      showlegend: false,
                      hoverinfo: "skip" as const,
                    },
                    {
                      type: "scatter" as const,
                      mode: "markers" as const,
                      y: [d.algorithmOrDataset],
                      x: [d.reference_compression_ratio],
                      marker: { color: "#aaaaaa", size: 8 },
                      name: "Best Compression",
                      hovertemplate: "Best: %{x:.2f}<extra></extra>",
                      showlegend:
                        d.algorithmOrDataset === data[0].algorithmOrDataset, // Only show legend for first point
                    },
                  ]),
              ]
            : []),
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
  algorithmOrDataset: string;
  compression_ratio: number;
  reference_compression_ratio: number | null; // the highest compression ratio for the dataset (if algorithmOrDataset is a dataset)
  encode_speed: number;
  decode_speed: number;
}

interface BenchmarkChartsProps {
  chartData: ChartData[];
  showSortByCompressionRatio?: boolean;
}

export function BenchmarkCharts({
  chartData,
  showSortByCompressionRatio,
}: BenchmarkChartsProps) {
  const [sortByRatio, setSortByRatio] = useState(
    showSortByCompressionRatio ? true : false,
  );

  console.log("--- showSortByCompressionRatio", showSortByCompressionRatio);

  if (!chartData.length) return null;

  const sortedData = sortByRatio
    ? [...chartData].sort((a, b) => a.compression_ratio - b.compression_ratio)
    : chartData;

  return (
    <div>
      {showSortByCompressionRatio && (
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
      )}
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
