function Datasets() {
  return (
    <div>
      <h1
        style={{
          fontSize: "2rem",
          fontWeight: "bold",
          color: "#333",
          marginBottom: "1rem",
        }}
      >
        Benchmark Datasets
      </h1>
      <div className="dataset-types">
        <section style={{ marginBottom: "2rem" }}>
          <h2 style={{ fontSize: "1.5rem", color: "#444", marginBottom: "1rem" }}>
            Bernoulli Datasets
          </h2>
          <p style={{ color: "#666", marginBottom: "1rem" }}>
            [Dataset description will be loaded from results.json]
          </p>
          <div style={{ color: "#666", marginLeft: "1rem" }}>
            <div>• bernoulli-0.1</div>
            <div>• bernoulli-0.2</div>
            <div>• bernoulli-0.3</div>
            <div>• bernoulli-0.4</div>
            <div>• bernoulli-0.5</div>
          </div>
        </section>

        <section style={{ marginBottom: "2rem" }}>
          <h2 style={{ fontSize: "1.5rem", color: "#444", marginBottom: "1rem" }}>
            Gaussian Datasets
          </h2>
          <p style={{ color: "#666", marginBottom: "1rem" }}>
            [Dataset description will be loaded from results.json]
          </p>
          <div style={{ color: "#666", marginLeft: "1rem" }}>
            <div>• gaussian-1</div>
            <div>• gaussian-2</div>
            <div>• gaussian-3</div>
            <div>• gaussian-5</div>
            <div>• gaussian-8</div>
          </div>
        </section>
      </div>
    </div>
  );
}

export default Datasets;
