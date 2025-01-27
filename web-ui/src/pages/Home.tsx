import { BenchmarkTable } from "../components/benchmark/table/BenchmarkTable";
import { BenchmarkData } from "../types";

interface HomeProps {
  benchmarkData: BenchmarkData | null;
}

function Home({ benchmarkData }: HomeProps) {
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
        {benchmarkData && <BenchmarkTable results={benchmarkData.results} />}
      </main>
    </div>
  );
}

export default Home;
