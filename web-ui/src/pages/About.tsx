import React from "react";
import ReactMarkdown from "react-markdown";
import { useMarkdownPosts } from "../hooks/useMarkdownPosts";

const About: React.FC = () => {
  const { posts, error, loading } = useMarkdownPosts("posts");

  return (
    <div style={{ maxWidth: "800px", margin: "0 auto" }}>
      <h1>About Benchcompress</h1>

      <p
        style={{ fontSize: "1.1rem", lineHeight: "1.6", marginBottom: "2rem" }}
      >
        Benchcompress is a benchmarking framework for evaluating compression
        algorithms on numeric timeseries datasets, with a focus on scientific
        data. It measures compression ratios and performance metrics across
        various algorithms and datasets.
      </p>

      <p>
        <a
          href="https://github.com/magland/benchcompress"
          target="_blank"
          rel="noopener noreferrer"
          style={{ color: "#0066cc" }}
        >
          View on GitHub
        </a>
      </p>

      <hr />

      {error ? (
        <div style={{ color: "red" }}>Error loading content: {error}</div>
      ) : loading ? (
        <div>Loading...</div>
      ) : (
        <div>
          {posts.map((post) => (
            <div
              key={post.path}
              className="markdown-content"
              style={{ marginBottom: "2rem" }}
            >
              <div style={{ color: "#666", marginBottom: "1rem" }}>
                {post.date.toLocaleDateString("en-US", {
                  year: "numeric",
                  month: "long",
                  day: "numeric",
                })}
              </div>
              <ReactMarkdown>{post.content}</ReactMarkdown>
              {post.path !== posts[posts.length - 1].path && <hr />}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default About;
