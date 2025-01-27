import { useParams } from "react-router-dom";
import { Algorithm as AlgorithmType } from "../types";

interface AlgorithmProps {
  algorithms: AlgorithmType[];
}

function Algorithm({ algorithms }: AlgorithmProps) {
  const { algorithmName } = useParams<{ algorithmName: string }>();
  const algorithm = algorithms.find((a) => a.name === algorithmName);

  if (!algorithm) {
    return <div>Algorithm not found</div>;
  }

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
        {algorithm.name}
      </h1>
      <div>
        <div style={{ marginBottom: "1.5rem" }}>
          <p style={{ fontSize: "0.9rem", lineHeight: "1.5" }}>
            {algorithm.description}
          </p>
        </div>
        <div style={{ marginBottom: "1.5rem" }}>
          <h2
            style={{
              fontSize: "1.2rem",
              fontWeight: "bold",
              marginBottom: "0.5rem",
            }}
          >
            Version
          </h2>
          <p style={{ fontSize: "0.9rem" }}>{algorithm.version}</p>
        </div>
        <div style={{ marginBottom: "1.5rem" }}>
          <h2
            style={{
              fontSize: "1.2rem",
              fontWeight: "bold",
              marginBottom: "0.5rem",
            }}
          >
            Tags
          </h2>
          <div>
            {algorithm.tags.map((tag) => (
              <span
                key={tag}
                style={{
                  display: "inline-block",
                  backgroundColor: "#e1e1e1",
                  padding: "2px 6px",
                  borderRadius: "3px",
                  margin: "2px",
                  fontSize: "0.8rem",
                }}
              >
                {tag}
              </span>
            ))}
          </div>
        </div>
        {algorithm.source_file && (
          <div style={{ marginBottom: "1.5rem" }}>
            <h2
              style={{
                fontSize: "1.2rem",
                fontWeight: "bold",
                marginBottom: "0.5rem",
              }}
            >
              Source
            </h2>
            <a
              href={algorithm.source_file}
              target="_blank"
              rel="noopener noreferrer"
              style={{
                color: "#0066cc",
                textDecoration: "none",
                padding: "4px 8px",
                backgroundColor: "#f0f0f0",
                borderRadius: "4px",
                fontSize: "0.9rem",
              }}
            >
              View Source
            </a>
          </div>
        )}
      </div>
    </div>
  );
}

export default Algorithm;
