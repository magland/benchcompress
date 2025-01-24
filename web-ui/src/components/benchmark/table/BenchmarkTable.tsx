import { useEffect, useState, useMemo } from "react";
import axios from "axios";
import {
  flexRender,
  getCoreRowModel,
  useReactTable,
  getSortedRowModel,
} from "@tanstack/react-table";
import { BenchmarkResult } from "../../../types";
import { columns } from "./columns";
import { BenchmarkCharts } from "../charts/BenchmarkCharts";
import { exportToCsv } from "../export/csvExport";

export function BenchmarkTable() {
  const [data, setData] = useState<BenchmarkResult[]>([]);
  const [selectedDataset, setSelectedDataset] = useState<string>("");
  const [availableDatasets, setAvailableDatasets] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsLoading(true);
        setError(null);
        const response = await axios.get(
          "https://raw.githubusercontent.com/magland/zia/benchmark-results/benchmark_results/results.json",
        );
        const results = response.data.results;
        setData(results);
        // Extract unique dataset names with proper typing
        const datasets = Array.from(
          new Set(results.map((result: BenchmarkResult) => result.dataset)),
        ).sort() as string[];
        setAvailableDatasets(datasets);
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

  // Memoize filtered data to prevent unnecessary recalculations
  const filteredData = useMemo(() => {
    if (!selectedDataset) return data;
    return data.filter((row) => row.dataset === selectedDataset);
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
      .filter((row) => row.dataset === selectedDataset)
      .map((row) => ({
        algorithm: row.algorithm,
        compression_ratio: row.compression_ratio,
        encode_speed: row.encode_mb_per_sec,
        decode_speed: row.decode_mb_per_sec,
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
      <div
        style={{
          marginBottom: "20px",
          display: "flex",
          alignItems: "center",
          gap: "10px",
          justifyContent: "space-between",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
          <label htmlFor="dataset-select">Dataset:</label>
          <select
            id="dataset-select"
            value={selectedDataset}
            onChange={(e) => setSelectedDataset(e.target.value)}
            style={{
              padding: "8px",
              borderRadius: "4px",
              border: "1px solid #ccc",
              minWidth: "200px",
              backgroundColor: "#fff",
            }}
          >
            <option value="">All Datasets</option>
            {availableDatasets.map((dataset) => (
              <option key={dataset} value={dataset}>
                {dataset}
              </option>
            ))}
          </select>
        </div>
        <button
          onClick={() => exportToCsv(filteredData, selectedDataset)}
          style={{
            padding: "8px 16px",
            backgroundColor: "#4CAF50",
            color: "white",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer",
            display: "flex",
            alignItems: "center",
            gap: "8px",
          }}
        >
          <svg
            width="16"
            height="16"
            viewBox="0 0 16 16"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path d="M8 12L3 7H6V1H10V7H13L8 12Z" fill="currentColor" />
            <path d="M2 14V15H14V14H2Z" fill="currentColor" />
          </svg>
          Download CSV
        </button>
      </div>

      {selectedDataset && chartData.length > 0 && (
        <BenchmarkCharts chartData={chartData} />
      )}

      <table>
        <thead>
          {table.getHeaderGroups().map((headerGroup) => (
            <tr key={headerGroup.id}>
              {headerGroup.headers.map((header) => (
                <th
                  key={header.id}
                  onClick={header.column.getToggleSortingHandler()}
                  style={{ cursor: "pointer" }}
                >
                  {flexRender(
                    header.column.columnDef.header,
                    header.getContext(),
                  )}
                  {header.column.getIsSorted() && (
                    <span style={{ marginLeft: "4px" }}>
                      {header.column.getIsSorted() === "asc" ? "↑" : "↓"}
                    </span>
                  )}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody>
          {table.getRowModel().rows.map((row) => (
            <tr key={row.id}>
              {row.getVisibleCells().map((cell) => (
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
