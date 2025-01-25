function Algorithms() {
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
        Compression Algorithms
      </h1>
      <div className="algorithms">
        <section style={{ marginBottom: "2rem" }}>
          <h2 style={{ fontSize: "1.5rem", color: "#444", marginBottom: "1rem" }}>
            Zlib
          </h2>
          <p style={{ color: "#666", marginBottom: "1rem" }}>
            [Algorithm description will be loaded from results.json]
          </p>
          <div style={{ color: "#666", marginLeft: "1rem" }}>
            <div>• zlib-1 (fastest)</div>
            <div>• zlib-3</div>
            <div>• zlib-5</div>
            <div>• zlib-7</div>
            <div>• zlib-9 (best compression)</div>
          </div>
        </section>

        <section style={{ marginBottom: "2rem" }}>
          <h2 style={{ fontSize: "1.5rem", color: "#444", marginBottom: "1rem" }}>
            Zstandard (zstd)
          </h2>
          <p style={{ color: "#666", marginBottom: "1rem" }}>
            [Algorithm description will be loaded from results.json]
          </p>
          <div style={{ color: "#666", marginLeft: "1rem" }}>
            <div>• zstd-4 (faster)</div>
            <div>• zstd-7</div>
            <div>• zstd-10</div>
            <div>• zstd-13</div>
            <div>• zstd-16</div>
            <div>• zstd-19</div>
            <div>• zstd-22 (better compression)</div>
          </div>
        </section>

        <section style={{ marginBottom: "2rem" }}>
          <h2 style={{ fontSize: "1.5rem", color: "#444", marginBottom: "1rem" }}>
            Simple ANS
          </h2>
          <p style={{ color: "#666", marginBottom: "1rem" }}>
            [Algorithm description will be loaded from results.json]
          </p>
        </section>
      </div>
    </div>
  );
}

export default Algorithms;
