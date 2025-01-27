import { useMemo } from "react";
import { BenchmarkResult } from "../types";

export function useBenchmarkChartData(
  results: BenchmarkResult[],
  selectedDataset?: string | null,
  selectedAlgorithm?: string | null,
) {
  return useMemo(() => {
    if (selectedDataset) {
      return results
        .filter((row) => row.dataset === selectedDataset)
        .map((row) => ({
          algorithm: row.algorithm,
          compression_ratio: row.compression_ratio,
          encode_speed: row.encode_mb_per_sec,
          decode_speed: row.decode_mb_per_sec,
        }));
    } else if (selectedAlgorithm) {
      return results
        .filter((row) => row.algorithm === selectedAlgorithm)
        .map((row) => ({
          algorithm: row.dataset,
          compression_ratio: row.compression_ratio,
          encode_speed: row.encode_mb_per_sec,
          decode_speed: row.decode_mb_per_sec,
        }));
    }
    return [];
  }, [results, selectedDataset, selectedAlgorithm]);
}
