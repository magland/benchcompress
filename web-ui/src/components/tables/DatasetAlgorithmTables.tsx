import { Link } from "react-router-dom";
import { TagFilter } from "../TagFilter";
import { Dataset, Algorithm } from "../../types";

interface DatasetTableProps {
  filteredDatasets: Dataset[];
  availableDatasetTags: string[];
  datasetTags: string[];
  toggleDatasetTag: (tag: string) => void;
}

interface AlgorithmTableProps {
  filteredAlgorithms: Algorithm[];
  availableAlgorithmTags: string[];
  algorithmTags: string[];
  toggleAlgorithmTag: (tag: string) => void;
}

export const DatasetTable = ({
  filteredDatasets,
  availableDatasetTags,
  datasetTags,
  toggleDatasetTag,
}: DatasetTableProps) => (
  <div style={{ overflowX: "auto" }}>
    <div style={{ marginBottom: "1rem" }}>
      <TagFilter
        availableTags={availableDatasetTags}
        selectedTags={datasetTags}
        onTagToggle={toggleDatasetTag}
        label="Filter datasets"
      />
    </div>
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
        {filteredDatasets.map((dataset, index) => (
          <tr
            key={`${dataset.name}-${dataset.version}`}
            style={{ backgroundColor: index % 2 === 0 ? "white" : "#fafafa" }}
          >
            <td
              style={{
                padding: "6px 12px",
                borderBottom: "1px solid #ddd",
                fontSize: "0.9rem",
              }}
            >
              <Link
                to={`/dataset/${encodeURIComponent(dataset.name)}`}
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
                  style={{ color: "#0066cc", textDecoration: "none" }}
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
              {dataset.data_url_npy && (
                <a
                  href={dataset.data_url_npy}
                  download={`${dataset.name}-${dataset.version}.npy`}
                  style={{ color: "#0066cc", textDecoration: "none" }}
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
);

export const AlgorithmTable = ({
  filteredAlgorithms,
  availableAlgorithmTags,
  algorithmTags,
  toggleAlgorithmTag,
}: AlgorithmTableProps) => (
  <div style={{ overflowX: "auto" }}>
    <div style={{ marginBottom: "1rem" }}>
      <TagFilter
        availableTags={availableAlgorithmTags}
        selectedTags={algorithmTags}
        onTagToggle={toggleAlgorithmTag}
        label="Filter algorithms"
      />
    </div>
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
            style={{ backgroundColor: index % 2 === 0 ? "white" : "#fafafa" }}
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
                  style={{ color: "#0066cc", textDecoration: "none" }}
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
);
