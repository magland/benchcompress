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
  availableDatasets: string[];
  availableAlgorithms: string[];
}

export function BenchmarkTable({
  results,
  availableDatasets,
  availableAlgorithms,
}: BenchmarkTableProps) {
  const [searchParams, setSearchParams] = useSearchParams();
  const selectedDataset = searchParams.get("dataset") || "";
  const selectedAlgorithm = searchParams.get("algorithm") || "";

  const filteredData = results;

  const table = useReactTable({
    data: filteredData || [],
    columns,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
  });

  const chartData = useMemo(() => {
    if (selectedDataset) {
      return filteredData
        .filter((row: BenchmarkResult) => row.dataset === selectedDataset)
        .map((row: BenchmarkResult) => ({
          algorithm: row.algorithm,
          compression_ratio: row.compression_ratio,
          encode_speed: row.encode_mb_per_sec,
          decode_speed: row.decode_mb_per_sec,
        }));
    } else if (selectedAlgorithm) {
      return filteredData
        .filter((row: BenchmarkResult) => row.algorithm === selectedAlgorithm)
        .map((row: BenchmarkResult) => ({
          algorithm: row.dataset,
          compression_ratio: row.compression_ratio,
          encode_speed: row.encode_mb_per_sec,
          decode_speed: row.decode_mb_per_sec,
        }));
    }
    return [];
  }, [filteredData, selectedDataset, selectedAlgorithm]);

  return (
    <div className="table-container">
      <div
        style={{
          marginBottom: "12px",
          display: "flex",
          alignItems: "center",
          gap: "8px",
          justifyContent: "space-between",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
            <label htmlFor="dataset-select">Dataset:</label>
            <select
              id="dataset-select"
              value={selectedDataset}
              onChange={(e) => {
                if (e.target.value) {
                  setSearchParams({ dataset: e.target.value });
                } else {
                  setSearchParams(
                    selectedAlgorithm ? { algorithm: selectedAlgorithm } : {},
                  );
                }
              }}
              style={{
                padding: "4px 8px",
                borderRadius: "4px",
                border: "1px solid #ccc",
                minWidth: "150px",
                backgroundColor: "#fff",
                fontSize: "0.9rem",
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
          <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
            <label htmlFor="algorithm-select">Algorithm:</label>
            <select
              id="algorithm-select"
              value={selectedAlgorithm}
              onChange={(e) => {
                if (e.target.value) {
                  setSearchParams({ algorithm: e.target.value });
                } else {
                  setSearchParams(
                    selectedDataset ? { dataset: selectedDataset } : {},
                  );
                }
              }}
              style={{
                padding: "4px 8px",
                borderRadius: "4px",
                border: "1px solid #ccc",
                minWidth: "150px",
                backgroundColor: "#fff",
                fontSize: "0.9rem",
              }}
            >
              <option value="">All Algorithms</option>
              {availableAlgorithms.map((algorithm) => (
                <option key={algorithm} value={algorithm}>
                  {algorithm}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {(selectedDataset || selectedAlgorithm) && chartData.length > 0 && (
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

      <div
        style={{
          marginTop: "12px",
          display: "flex",
          justifyContent: "flex-end",
        }}
      >
        <button
          onClick={() =>
            exportToCsv(filteredData, selectedDataset || selectedAlgorithm)
          }
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
    </div>
  );
}
