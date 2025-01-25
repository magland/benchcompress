import { BenchmarkTable } from "../components/BenchmarkTable";

function Home() {
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
          Comparing different integer array compression algorithms and their
          performance
        </p>
        <a
          href="https://github.com/magland/zia"
          target="_blank"
          rel="noopener noreferrer"
          style={{
            color: "#0066cc",
            textDecoration: "none",
            display: "inline-block",
            marginTop: "0.5rem",
          }}
        >
          View source on GitHub
        </a>
      </header>
      <main>
        <BenchmarkTable />
      </main>
    </div>
  );
}

export default Home;
