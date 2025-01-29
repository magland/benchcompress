import React from "react";
import ReactMarkdown from "react-markdown";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
// Import paper.md from project root paper/ directory
import paperContent from "../../../paper/paper.md?raw";
import "katex/dist/katex.min.css";
import "./Paper.css";

const Paper: React.FC = () => {
  return (
    <div className="paper-container">
      <div className="paper-content">
        <ReactMarkdown
          remarkPlugins={[remarkMath]}
          rehypePlugins={[rehypeKatex]}
        >
          {paperContent}
        </ReactMarkdown>
      </div>
    </div>
  );
};

export default Paper;
