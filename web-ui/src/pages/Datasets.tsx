import { Dataset } from "../types";
import { Link } from "react-router-dom";

interface DatasetsProps {
  datasets: Dataset[];
}

function Datasets({ datasets }: DatasetsProps) {
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
      <div style={{ overflowX: "auto" }}>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr style={{ backgroundColor: "#f5f5f5" }}>
              <th
                style={{
                  padding: "12px",
                  textAlign: "left",
                  borderBottom: "2px solid #ddd",
                }}
              >
                Name
              </th>
              <th
                style={{
                  padding: "12px",
                  textAlign: "left",
                  borderBottom: "2px solid #ddd",
                }}
              >
                Version
              </th>
              <th
                style={{
                  padding: "12px",
                  textAlign: "left",
                  borderBottom: "2px solid #ddd",
                }}
              >
                Description
              </th>
              <th
                style={{
                  padding: "12px",
                  textAlign: "left",
                  borderBottom: "2px solid #ddd",
                }}
              >
                Tags
              </th>
              <th
                style={{
                  padding: "12px",
                  textAlign: "left",
                  borderBottom: "2px solid #ddd",
                }}
              >
                Source
              </th>
            </tr>
          </thead>
          <tbody>
            {datasets.map((dataset, index) => (
              <tr
                key={`${dataset.name}-${dataset.version}`}
                style={{
                  backgroundColor: index % 2 === 0 ? "white" : "#fafafa",
                }}
              >
                <td style={{ padding: "12px", borderBottom: "1px solid #ddd" }}>
                  <Link
                    to={`/home?dataset=${encodeURIComponent(dataset.name)}`}
                    style={{
                      color: "#0066cc",
                      textDecoration: "none",
                      fontWeight: "500",
                    }}
                  >
                    {dataset.name}
                  </Link>
                </td>
                <td style={{ padding: "12px", borderBottom: "1px solid #ddd" }}>
                  {dataset.version}
                </td>
                <td style={{ padding: "12px", borderBottom: "1px solid #ddd" }}>
                  {dataset.description}
                </td>
                <td style={{ padding: "12px", borderBottom: "1px solid #ddd" }}>
                  {dataset.tags.map((tag) => (
                    <span
                      key={tag}
                      style={{
                        display: "inline-block",
                        backgroundColor: "#e1e1e1",
                        padding: "4px 8px",
                        borderRadius: "4px",
                        margin: "2px",
                        fontSize: "0.9em",
                      }}
                    >
                      {tag}
                    </span>
                  ))}
                </td>
                <td style={{ padding: "12px", borderBottom: "1px solid #ddd" }}>
                  {dataset.source_file && (
                    <a
                      href={dataset.source_file}
                      target="_blank"
                      rel="noopener noreferrer"
                      style={{
                        color: "#0066cc",
                        textDecoration: "none",
                      }}
                    >
                      View Source
                    </a>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Datasets;
