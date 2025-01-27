import { BenchmarkTable } from "../components/benchmark/table/BenchmarkTable";
import { BenchmarkData } from "../types";
import { useSearchParams } from "react-router-dom";
import { useMemo } from "react";
import { TagFilter } from "../components/TagFilter";
import { useTagFilter } from "../hooks/useTagFilter";

interface HomeProps {
  benchmarkData: BenchmarkData | null;
}

function Home({ benchmarkData }: HomeProps) {
  const [searchParams] = useSearchParams();
  const selectedDataset = searchParams.get("dataset") || "";
  const selectedAlgorithm = searchParams.get("algorithm") || "";

  // Set up tag filtering for datasets
  const {
    selectedTags: selectedDatasetTags,
    availableTags: availableDatasetTags,
    filteredItems: filteredDatasets,
    toggleTag: toggleDatasetTag,
  } = useTagFilter(benchmarkData?.datasets || []);

  // Set up tag filtering for algorithms
  const {
    selectedTags: selectedAlgorithmTags,
    availableTags: availableAlgorithmTags,
    filteredItems: filteredAlgorithms,
    toggleTag: toggleAlgorithmTag,
  } = useTagFilter(benchmarkData?.algorithms || []);

  // Filter benchmark results based on selected dataset/algorithm and tags
  const filteredResults = useMemo(() => {
    if (!benchmarkData) return [];

    let filtered = benchmarkData.results;

    // Filter by selected dataset/algorithm
    if (selectedDataset) {
      filtered = filtered.filter(
        (result) => result.dataset === selectedDataset,
      );
    } else if (selectedDatasetTags.length > 0) {
      // Only apply dataset tag filtering if no specific dataset is selected
      const datasetNames = filteredDatasets.map((d) => d.name);
      filtered = filtered.filter((result) =>
        datasetNames.includes(result.dataset),
      );
    }

    if (selectedAlgorithm) {
      filtered = filtered.filter(
        (result) => result.algorithm === selectedAlgorithm,
      );
    } else if (selectedAlgorithmTags.length > 0) {
      // Only apply algorithm tag filtering if no specific algorithm is selected
      const algorithmNames = filteredAlgorithms.map((a) => a.name);
      filtered = filtered.filter((result) =>
        algorithmNames.includes(result.algorithm),
      );
    }

    return filtered;
  }, [
    benchmarkData,
    selectedDataset,
    selectedAlgorithm,
    selectedDatasetTags,
    selectedAlgorithmTags,
    filteredDatasets,
    filteredAlgorithms,
  ]);

  return (
    <div>
      <header style={{ marginBottom: "2rem" }}>
        <h1
          style={{
            fontSize: "2rem",
            fontWeight: "bold",
            color: "#333",
          }}
        >
          Integer Compression Benchmark
        </h1>
        <p
          style={{
            color: "#666",
            marginTop: "0.5rem",
          }}
        >
          Comparing numeric array compression algorithms
        </p>
      </header>
      <main>
        <div
          style={{
            marginBottom: "2rem",
            display: "flex",
            flexDirection: "column",
            gap: "1rem",
          }}
        >
          {!selectedDataset && (
            <TagFilter
              availableTags={availableDatasetTags}
              selectedTags={selectedDatasetTags}
              onTagToggle={toggleDatasetTag}
              label="Filter datasets"
            />
          )}

          {!selectedAlgorithm && (
            <TagFilter
              availableTags={availableAlgorithmTags}
              selectedTags={selectedAlgorithmTags}
              onTagToggle={toggleAlgorithmTag}
              label="Filter algorithms"
            />
          )}
        </div>

        {benchmarkData && (
          <BenchmarkTable
            results={filteredResults}
            availableDatasets={filteredDatasets.map((d) => d.name)}
            availableAlgorithms={filteredAlgorithms.map((a) => a.name)}
          />
        )}
      </main>
    </div>
  );
}

export default Home;
