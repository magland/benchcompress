import { useEffect, useState, useMemo } from 'react';
import axios from 'axios';
import Plot from 'react-plotly.js';
import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  useReactTable,
  getSortedRowModel,
} from '@tanstack/react-table';
import { BenchmarkResult } from '../types';

const columnHelper = createColumnHelper<BenchmarkResult>();

const formatNumber = (num: number, decimals = 2) => {
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(num);
};

const formatSize = (bytes: number) => {
  const mb = bytes / (1024 * 1024);
  return `${formatNumber(mb)} MB`;
};

const columns = [
  columnHelper.accessor('dataset', {
    header: 'Dataset',
    cell: info => info.getValue(),
  }),
  columnHelper.accessor('algorithm', {
    header: 'Algorithm',
    cell: info => info.getValue(),
  }),
  columnHelper.accessor('compression_ratio', {
    header: 'Compression Ratio',
    cell: info => `${formatNumber(info.getValue())}x`,
    sortingFn: (rowA, rowB) => {
      const a = rowA.original.compression_ratio;
      const b = rowB.original.compression_ratio;
      return a - b;
    },
  }),
  columnHelper.accessor('encode_time', {
    header: 'Encode Time (s)',
    cell: info => formatNumber(info.getValue(), 4),
    sortingFn: (rowA, rowB) => {
      const a = rowA.original.encode_time;
      const b = rowB.original.encode_time;
      return a - b;
    },
  }),
  columnHelper.accessor('decode_time', {
    header: 'Decode Time (s)',
    cell: info => formatNumber(info.getValue(), 4),
    sortingFn: (rowA, rowB) => {
      const a = rowA.original.decode_time;
      const b = rowB.original.decode_time;
      return a - b;
    },
  }),
  columnHelper.accessor('encode_mb_per_sec', {
    header: 'Encode Speed (MB/s)',
    cell: info => formatNumber(info.getValue()),
    sortingFn: (rowA, rowB) => {
      const a = rowA.original.encode_mb_per_sec;
      const b = rowB.original.encode_mb_per_sec;
      return a - b;
    },
  }),
  columnHelper.accessor('decode_mb_per_sec', {
    header: 'Decode Speed (MB/s)',
    cell: info => formatNumber(info.getValue()),
    sortingFn: (rowA, rowB) => {
      const a = rowA.original.decode_mb_per_sec;
      const b = rowB.original.decode_mb_per_sec;
      return a - b;
    },
  }),
  columnHelper.accessor('original_size', {
    header: 'Original Size',
    cell: info => formatSize(info.getValue()),
    sortingFn: (rowA, rowB) => {
      const a = rowA.original.original_size;
      const b = rowB.original.original_size;
      return a - b;
    },
  }),
  columnHelper.accessor('compressed_size', {
    header: 'Compressed Size',
    cell: info => formatSize(info.getValue()),
    sortingFn: (rowA, rowB) => {
      const a = rowA.original.compressed_size;
      const b = rowB.original.compressed_size;
      return a - b;
    },
  }),
];

export function BenchmarkTable() {
  const [data, setData] = useState<BenchmarkResult[]>([]);
  const [selectedDataset, setSelectedDataset] = useState<string>('');
  const [availableDatasets, setAvailableDatasets] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsLoading(true);
        setError(null);
        const response = await axios.get(
          'https://raw.githubusercontent.com/magland/zia/benchmark-results/benchmark_results/results.json'
        );
        const results = response.data.results;
        setData(results);
        // Extract unique dataset names with proper typing
        const datasets = Array.from(new Set(results.map((result: BenchmarkResult) => result.dataset))).sort() as string[];
        setAvailableDatasets(datasets);
      } catch (error) {
        const message = error instanceof Error ? error.message : 'Failed to fetch data';
        setError(message);
        console.error('Error fetching benchmark data:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  // Memoize filtered data to prevent unnecessary recalculations
  const filteredData = useMemo(() => {
    if (!selectedDataset) return data;
    return data.filter(row => row.dataset === selectedDataset);
  }, [data, selectedDataset]);

  const table = useReactTable({
    data: filteredData || [],
    columns,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
  });

  // Prepare data for bar charts when a dataset is selected
  const chartData = useMemo(() => {
    if (!selectedDataset) return [];
    return data
      .filter(row => row.dataset === selectedDataset)
      .map(row => ({
        algorithm: row.algorithm,
        compression_ratio: row.compression_ratio,
        encode_speed: row.encode_mb_per_sec,
        decode_speed: row.decode_mb_per_sec
      }));
  }, [data, selectedDataset]);

  if (isLoading) {
    return <div>Loading benchmark data...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div className="table-container">
      <div style={{ marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '10px' }}>
        <label htmlFor="dataset-select">Filter by Dataset:</label>
        <select
          id="dataset-select"
          value={selectedDataset}
          onChange={(e) => setSelectedDataset(e.target.value)}
          style={{
            padding: '8px',
            borderRadius: '4px',
            border: '1px solid #ccc',
            minWidth: '200px',
            backgroundColor: '#fff'
          }}
        >
          <option value="">All Datasets</option>
          {availableDatasets.map(dataset => (
            <option key={dataset} value={dataset}>
              {dataset}
            </option>
          ))}
        </select>
      </div>

      {selectedDataset && chartData.length > 0 && (
        <div style={{ marginBottom: '30px' }}>
          <div style={{ marginBottom: '20px' }}>
            <h3 style={{ marginBottom: '10px' }}>Compression Ratio</h3>
            <Plot
              data={[{
                type: 'bar',
                x: chartData.map(d => d.algorithm),
                y: chartData.map(d => d.compression_ratio),
                marker: { color: '#8884d8' }
              }]}
              layout={{
                width: 800,
                height: 300,
                margin: { t: 5, r: 30, l: 50, b: 30 },
                yaxis: { title: 'Ratio' }
              }}
              config={{ displayModeBar: false }}
            />
          </div>

          <div style={{ marginBottom: '20px' }}>
            <h3 style={{ marginBottom: '10px' }}>Encode Speed (MB/s)</h3>
            <Plot
              data={[{
                type: 'bar',
                x: chartData.map(d => d.algorithm),
                y: chartData.map(d => d.encode_speed),
                marker: { color: '#82ca9d' }
              }]}
              layout={{
                width: 800,
                height: 300,
                margin: { t: 5, r: 30, l: 50, b: 30 },
                yaxis: { title: 'MB/s' }
              }}
              config={{ displayModeBar: false }}
            />
          </div>

          <div style={{ marginBottom: '20px' }}>
            <h3 style={{ marginBottom: '10px' }}>Decode Speed (MB/s)</h3>
            <Plot
              data={[{
                type: 'bar',
                x: chartData.map(d => d.algorithm),
                y: chartData.map(d => d.decode_speed),
                marker: { color: '#ff7300' }
              }]}
              layout={{
                width: 800,
                height: 300,
                margin: { t: 5, r: 30, l: 50, b: 30 },
                yaxis: { title: 'MB/s' }
              }}
              config={{ displayModeBar: false }}
            />
          </div>
        </div>
      )}
      <table>
        <thead>
          {table.getHeaderGroups().map(headerGroup => (
            <tr key={headerGroup.id}>
              {headerGroup.headers.map(header => (
                <th
                  key={header.id}
                  onClick={header.column.getToggleSortingHandler()}
                  style={{ cursor: 'pointer' }}
                >
                  {flexRender(
                    header.column.columnDef.header,
                    header.getContext()
                  )}
                  {header.column.getIsSorted() && (
                    <span style={{ marginLeft: '4px' }}>
                      {header.column.getIsSorted() === 'asc' ? '↑' : '↓'}
                    </span>
                  )}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody>
          {table.getRowModel().rows.map(row => (
            <tr key={row.id}>
              {row.getVisibleCells().map(cell => (
                <td key={cell.id}>
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
