#!/bin/bash

cd "$(dirname "$0")/.."
cd paper

pandoc paper.md \
  --bibliography=references.bib \
  -o paper.pdf

echo "Paper compiled successfully to paper.pdf"
