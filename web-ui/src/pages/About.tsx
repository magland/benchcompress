import React from "react";

const About: React.FC = () => {
  return (
    <div style={{ maxWidth: "800px", margin: "0 auto" }}>
      <h1>About Zia</h1>

      <p
        style={{ fontSize: "1.1rem", lineHeight: "1.6", marginBottom: "2rem" }}
      >
        Zia is a benchmarking framework for evaluating compression algorithms on
        integer array datasets, with a focus on scientific data. It measures
        compression ratios and performance metrics across various algorithms and
        datasets.
      </p>

      <p>
        <a
          href="https://github.com/magland/zia"
          target="_blank"
          rel="noopener noreferrer"
          style={{ color: "#0066cc" }}
        >
          View on GitHub
        </a>
      </p>
    </div>
  );
};

export default About;
