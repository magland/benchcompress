import { Algorithm } from "../types";
import { Link } from "react-router-dom";
import { TagFilter } from "../components/TagFilter";
import { useTagFilter } from "../hooks/useTagFilter";

interface AlgorithmsProps {
  algorithms: Algorithm[];
}

function Algorithms({ algorithms }: AlgorithmsProps) {
  const {
    selectedTags,
    availableTags,
    filteredItems: filteredAlgorithms,
    toggleTag,
  } = useTagFilter(algorithms);

  return (
    <div>
      <div style={{ marginBottom: "2rem" }}>
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
        <TagFilter
          availableTags={availableTags}
          selectedTags={selectedTags}
          onTagToggle={toggleTag}
          label="Filter algorithms"
        />
      </div>
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
            </tr>
          </thead>
          <tbody>
            {filteredAlgorithms.map((algorithm, index) => (
              <tr
                key={`${algorithm.name}-${algorithm.version}`}
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
                    to={`/algorithm/${encodeURIComponent(algorithm.name)}`}
                    style={{
                      color: "#0066cc",
                      textDecoration: "none",
                      fontWeight: "500",
                    }}
                  >
                    {algorithm.name}
                  </Link>
                </td>
                <td
                  style={{
                    padding: "6px 12px",
                    borderBottom: "1px solid #ddd",
                    fontSize: "0.9rem",
                  }}
                >
                  {algorithm.version}
                </td>
                <td
                  style={{
                    padding: "6px 12px",
                    borderBottom: "1px solid #ddd",
                    fontSize: "0.9rem",
                  }}
                >
                  {algorithm.description}
                </td>
                <td
                  style={{
                    padding: "6px 12px",
                    borderBottom: "1px solid #ddd",
                    fontSize: "0.9rem",
                  }}
                >
                  {algorithm.tags.map((tag) => (
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
                  {algorithm.source_file && (
                    <a
                      href={algorithm.source_file}
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

export default Algorithms;
