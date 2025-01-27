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
  const [searchParams, setSearchParams] = useSearchParams();
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
          Benchmark Results
        </h1>
        <p
          style={{
            color: "#666",
            marginTop: "0.5rem",
          }}
        >
          Comparing compression algorithms for numeric arrays
        </p>
      </header>
      <main>
        <div style={{ marginBottom: "2rem" }}>
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "12px",
              marginBottom: "1rem",
            }}
          >
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
                {filteredDatasets.map((dataset) => (
                  <option key={dataset.name} value={dataset.name}>
                    {dataset.name}
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
                {filteredAlgorithms.map((algorithm) => (
                  <option key={algorithm.name} value={algorithm.name}>
                    {algorithm.name}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div
            style={{ display: "flex", flexDirection: "column", gap: "1rem" }}
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
        </div>

        {benchmarkData && <BenchmarkTable results={filteredResults} />}
      </main>
    </div>
  );
}

export default Home;
