import { useParams } from "react-router-dom";
import { Dataset as DatasetType } from "../types";
import TimeseriesView from "../components/dataset/TimeseriesView";

interface DatasetProps {
  datasets: DatasetType[];
}

function Dataset({ datasets }: DatasetProps) {
  const { datasetName } = useParams<{ datasetName: string }>();
  const dataset = datasets.find((d) => d.name === datasetName);

  if (!dataset) {
    return <div>Dataset not found</div>;
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
        {dataset.name}
      </h1>
      <div style={{ maxWidth: "800px", margin: "0 auto" }}>
        <div style={{ marginBottom: "1.5rem" }}>
          <h2
            style={{
              fontSize: "1.2rem",
              fontWeight: "bold",
              marginBottom: "0.5rem",
            }}
          >
            Description
          </h2>
          <p style={{ fontSize: "0.9rem", lineHeight: "1.5" }}>
            {dataset.description}
          </p>
        </div>
        <div style={{ marginBottom: "1.5rem" }}>
          <div
            style={{
              width: "100%",
              height: "300px",
              backgroundColor: "#f5f5f5",
              borderRadius: "4px",
              padding: "1rem",
            }}
          >
            <TimeseriesView width={700} height={250} dataset={dataset} />
          </div>
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
          <p style={{ fontSize: "0.9rem" }}>{dataset.version}</p>
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
            {dataset.tags.map((tag) => (
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
        <div style={{ marginBottom: "1.5rem" }}>
          <h2
            style={{
              fontSize: "1.2rem",
              fontWeight: "bold",
              marginBottom: "0.5rem",
            }}
          >
            Downloads
          </h2>
          <div style={{ display: "flex", gap: "1rem" }}>
            {dataset.data_url_npy && (
              <a
                href={dataset.data_url_npy}
                download={`${dataset.name}-${dataset.version}.npy`}
                style={{
                  color: "#0066cc",
                  textDecoration: "none",
                  padding: "4px 8px",
                  backgroundColor: "#f0f0f0",
                  borderRadius: "4px",
                  fontSize: "0.9rem",
                }}
              >
                Download NPY
              </a>
            )}
            {dataset.data_url_raw && (
              <a
                href={dataset.data_url_raw}
                download={`${dataset.name}-${dataset.version}.dat`}
                style={{
                  color: "#0066cc",
                  textDecoration: "none",
                  padding: "4px 8px",
                  backgroundColor: "#f0f0f0",
                  borderRadius: "4px",
                  fontSize: "0.9rem",
                }}
              >
                Download RAW
              </a>
            )}
          </div>
        </div>
        {dataset.source_file && (
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
              href={dataset.source_file}
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

export default Dataset;
