import { useMemo } from "react";
import { useSearchParams } from "react-router-dom";
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

interface BenchmarkTableProps {
  results: BenchmarkResult[];
}

export function BenchmarkTable({ results }: BenchmarkTableProps) {
  const [searchParams, setSearchParams] = useSearchParams();
  const selectedDataset = searchParams.get("dataset") || "";
  const availableDatasets = useMemo(() => {
    return Array.from(new Set(results.map((result) => result.dataset))).sort();
  }, [results]);

  // Memoize filtered data to prevent unnecessary recalculations
  const filteredData = useMemo(() => {
    if (!selectedDataset) return results;
    return results.filter((row) => row.dataset === selectedDataset);
  }, [results, selectedDataset]);

  const table = useReactTable({
    data: filteredData || [],
    columns,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
  });

  // Prepare data for bar charts when a dataset is selected
  const chartData = useMemo(() => {
    if (!selectedDataset) return [];
    return results
      .filter((row: BenchmarkResult) => row.dataset === selectedDataset)
      .map((row: BenchmarkResult) => ({
        algorithm: row.algorithm,
        compression_ratio: row.compression_ratio,
        encode_speed: row.encode_mb_per_sec,
        decode_speed: row.decode_mb_per_sec,
      }));
  }, [results, selectedDataset]);

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
            onChange={(e) => {
              if (e.target.value) {
                setSearchParams({ dataset: e.target.value });
              } else {
                setSearchParams({});
              }
            }}
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
