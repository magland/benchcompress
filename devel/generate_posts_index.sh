#!/bin/bash

# Directory containing this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Path to the posts directory relative to the script location
POSTS_DIR="$SCRIPT_DIR/../web-ui/public/posts"
INDEX_FILE="$POSTS_DIR/index.txt"

# Create posts directory if it doesn't exist
mkdir -p "$POSTS_DIR"

# Find all .md files in the posts directory and write to index.txt
find "$POSTS_DIR" -maxdepth 1 -name "*.md" -type f -printf "%f\n" | sort > "$INDEX_FILE"

echo "Generated posts index at $INDEX_FILE"
