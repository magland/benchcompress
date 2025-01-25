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
                  padding: "8px 12px",
                  textAlign: "left",
                  borderBottom: "1px solid #ddd",
                  fontSize: "0.9rem",
                  whiteSpace: "nowrap",
                }}
              >
                Name
              </th>
              <th
                style={{
                  padding: "8px 12px",
                  textAlign: "left",
                  borderBottom: "1px solid #ddd",
                  fontSize: "0.9rem",
                  whiteSpace: "nowrap",
                }}
              >
                Version
              </th>
              <th
                style={{
                  padding: "8px 12px",
                  textAlign: "left",
                  borderBottom: "1px solid #ddd",
                  fontSize: "0.9rem",
                  whiteSpace: "nowrap",
                }}
              >
                Description
              </th>
              <th
                style={{
                  padding: "8px 12px",
                  textAlign: "left",
                  borderBottom: "1px solid #ddd",
                  fontSize: "0.9rem",
                  whiteSpace: "nowrap",
                }}
              >
                Tags
              </th>
              <th
                style={{
                  padding: "8px 12px",
                  textAlign: "left",
                  borderBottom: "1px solid #ddd",
                  fontSize: "0.9rem",
                  whiteSpace: "nowrap",
                }}
              >
                Source
              </th>
              <th
                style={{
                  padding: "8px 12px",
                  textAlign: "left",
                  borderBottom: "1px solid #ddd",
                  fontSize: "0.9rem",
                  whiteSpace: "nowrap",
                }}
              >
                Data
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
                <td
                  style={{
                    padding: "6px 12px",
                    borderBottom: "1px solid #ddd",
                    fontSize: "0.9rem",
                  }}
                >
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
                <td
                  style={{
                    padding: "6px 12px",
                    borderBottom: "1px solid #ddd",
                    fontSize: "0.9rem",
                  }}
                >
                  {dataset.version}
                </td>
                <td
                  style={{
                    padding: "6px 12px",
                    borderBottom: "1px solid #ddd",
                    fontSize: "0.9rem",
                  }}
                >
                  {dataset.description}
                </td>
                <td
                  style={{
                    padding: "6px 12px",
                    borderBottom: "1px solid #ddd",
                    fontSize: "0.9rem",
                  }}
                >
                  {dataset.tags.map((tag) => (
                    <span
                      key={tag}
                      style={{
                        display: "inline-block",
                        backgroundColor: "#e1e1e1",
                        padding: "2px 6px",
                        borderRadius: "3px",
                        margin: "1px",
                        fontSize: "0.8rem",
                      }}
                    >
                      {tag}
                    </span>
                  ))}
                </td>
                <td
                  style={{
                    padding: "6px 12px",
                    borderBottom: "1px solid #ddd",
                    fontSize: "0.9rem",
                  }}
                >
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
                <td
                  style={{
                    padding: "6px 12px",
                    borderBottom: "1px solid #ddd",
                    fontSize: "0.9rem",
                  }}
                >
                  {dataset.data_url && (
                    <a
                      href={dataset.data_url}
                      download={`${dataset.name}-${dataset.version}.bin`}
                      style={{
                        color: "#0066cc",
                        textDecoration: "none",
                      }}
                    >
                      Download
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
