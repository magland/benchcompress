import Plot from 'react-plotly.js';

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
  if (!chartData.length) return null;

  return (
    <div style={{ marginBottom: '30px' }}>
      <div style={{ marginBottom: '20px' }}>
        <h3 style={{ marginBottom: '10px' }}>Compression Ratio</h3>
        <Plot
          data={[{
            type: 'bar',
            orientation: 'h',
            y: chartData.map(d => d.algorithm),
            x: chartData.map(d => d.compression_ratio),
            marker: { color: '#8884d8' }
          }]}
          layout={{
            width: 800,
            height: 400,
            margin: { t: 5, r: 30, l: 120, b: 30 },
            xaxis: { title: 'Ratio' }
          }}
          config={{ displayModeBar: false }}
        />
      </div>

      <div style={{ marginBottom: '20px' }}>
        <h3 style={{ marginBottom: '10px' }}>Encode Speed (MB/s)</h3>
        <Plot
          data={[{
            type: 'bar',
            orientation: 'h',
            y: chartData.map(d => d.algorithm),
            x: chartData.map(d => d.encode_speed),
            marker: { color: '#82ca9d' }
          }]}
          layout={{
            width: 800,
            height: 400,
            margin: { t: 5, r: 30, l: 120, b: 30 },
            xaxis: { title: 'MB/s' }
          }}
          config={{ displayModeBar: false }}
        />
      </div>

      <div style={{ marginBottom: '20px' }}>
        <h3 style={{ marginBottom: '10px' }}>Decode Speed (MB/s)</h3>
        <Plot
          data={[{
            type: 'bar',
            orientation: 'h',
            y: chartData.map(d => d.algorithm),
            x: chartData.map(d => d.decode_speed),
            marker: { color: '#ff7300' }
          }]}
          layout={{
            width: 800,
            height: 400,
            margin: { t: 5, r: 30, l: 120, b: 30 },
            xaxis: { title: 'MB/s' }
          }}
          config={{ displayModeBar: false }}
        />
      </div>
    </div>
  );
}
