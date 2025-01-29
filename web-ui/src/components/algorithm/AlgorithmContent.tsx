import { Algorithm, BenchmarkData } from "../../types";
import { BaseContent } from "../shared/BaseContent";
import "../shared/ContentStyles.css";

interface AlgorithmContentProps {
  algorithm: Algorithm;
  benchmarkData: BenchmarkData | null;
  chartData: Array<{
    algorithm: string;
    compression_ratio: number;
    encode_speed: number;
    decode_speed: number;
  }>;
}

export const AlgorithmContent = ({
  algorithm,
  benchmarkData,
  chartData,
}: AlgorithmContentProps) => {
  return (
    <BaseContent
      item={algorithm}
      benchmarkData={benchmarkData}
      chartData={chartData}
      tagNavigationPrefix="/algorithms"
      filterKey="algorithm"
    />
  );
};
