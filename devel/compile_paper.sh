#!/bin/bash

cd "$(dirname "$0")/.."
cd paper

pandoc paper.md \
  --metadata-file=paper.yml \
  --bibliography=references.bib \
  --csl=ieee.csl \
  -o paper.pdf

echo "Paper compiled successfully to paper.pdf"
