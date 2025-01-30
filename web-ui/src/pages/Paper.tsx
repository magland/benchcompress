import React from "react";
import "./Paper.css";

const Paper: React.FC = () => {
  return (
    <div className="paper-container">
      <div className="paper-content">
        <iframe
          src="/benchcompress/paper.pdf#toolbar=0&navpanes=0"
          width="100%"
          height="100%"
          style={{ minHeight: "100vh", border: "none" }}
        />
      </div>
    </div>
  );
};

export default Paper;
