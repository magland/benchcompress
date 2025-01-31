#!/bin/bash

# Exit on error
set -e

# Get the directory containing this script
cd "$(dirname "$0")/.."

# First compile the paper
./devel/compile_paper.sh

# Then copy it to web-ui/public/
cp paper/paper.pdf web-ui/public/

echo "Paper copied to web-ui/public/paper.pdf"
