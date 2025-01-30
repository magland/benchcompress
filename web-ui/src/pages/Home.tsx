import React from "react";
import { Link } from "react-router-dom";
import yaml from "yaml";
import contentYaml from "../content/home-content.yml?raw";
import { HomeContent, HomeSection } from "../types/home-content";
import "../components/Button.css";

const content = yaml.parse(contentYaml) as HomeContent;

const SectionCard: React.FC<{ section: HomeSection }> = ({ section }) => {
  if (section.external) {
    return (
      <div
        style={{
          padding: "1.5rem",
          border: "1px solid #eaeaea",
          borderRadius: "8px",
          backgroundColor: "#f9f9f9",
        }}
      >
        <h2 style={{ marginBottom: "1rem" }}>{section.title}</h2>
        <p style={{ marginBottom: "1rem" }}>{section.description}</p>
        <a
          href={section.link}
          target="_blank"
          rel="noopener noreferrer"
          className="soft-button"
        >
          {section.linkText}
        </a>
      </div>
    );
  }

  return (
    <div
      style={{
        padding: "1.5rem",
        border: "1px solid #eaeaea",
        borderRadius: "8px",
        backgroundColor: "#f9f9f9",
      }}
    >
      <h2 style={{ marginBottom: "1rem" }}>{section.title}</h2>
      <p style={{ marginBottom: "1rem" }}>{section.description}</p>
      <Link to={section.link} className="soft-button">
        {section.linkText}
      </Link>
    </div>
  );
};

export default function Home() {
  return (
    <div style={{ maxWidth: "1200px", margin: "0 auto", padding: "2rem" }}>
      <h1 style={{ marginBottom: "2rem" }}>{content.title}</h1>

      <p
        style={{ fontSize: "1.1rem", lineHeight: "1.6", marginBottom: "2rem" }}
      >
        {content.description}
      </p>

      <div
        style={{
          display: "grid",
          gap: "2rem",
          gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))",
        }}
      >
        {Object.entries(content.sections).map(([key, section]) => (
          <SectionCard key={key} section={section} />
        ))}
      </div>

      <hr
        style={{
          margin: "3rem 0",
          border: "none",
          borderTop: "1px solid #eaeaea",
        }}
      />

      <footer
        style={{ textAlign: "center", color: "#666", fontSize: "0.9rem" }}
      >
        <p>
          Last updated: {__BUILD_DATE__}
          <br />
          Released under{" "}
          <a
            href="https://github.com/magland/benchcompress/blob/main/LICENSE"
            target="_blank"
            rel="noopener noreferrer"
            style={{ color: "#666", textDecoration: "underline" }}
          >
            Apache License 2.0
          </a>
        </p>
      </footer>
    </div>
  );
}
