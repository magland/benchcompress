import { Algorithm } from "../types";

interface AlgorithmsProps {
  algorithms: Algorithm[];
}

function Algorithms({ algorithms }: AlgorithmsProps) {
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
            </tr>
          </thead>
          <tbody>
            {algorithms.map((algorithm, index) => (
              <tr
                key={`${algorithm.name}-${algorithm.version}`}
                style={{
                  backgroundColor: index % 2 === 0 ? "white" : "#fafafa",
                }}
              >
                <td style={{ padding: "12px", borderBottom: "1px solid #ddd" }}>
                  {algorithm.name}
                </td>
                <td style={{ padding: "12px", borderBottom: "1px solid #ddd" }}>
                  {algorithm.version}
                </td>
                <td style={{ padding: "12px", borderBottom: "1px solid #ddd" }}>
                  {algorithm.description}
                </td>
                <td style={{ padding: "12px", borderBottom: "1px solid #ddd" }}>
                  {algorithm.tags.map((tag) => (
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
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Algorithms;
