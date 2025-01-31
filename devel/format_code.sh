#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Format Python code
echo "Formatting Python code..."
black "$PROJECT_ROOT/benchcompress/src/benchcompress"

# Format TypeScript/JavaScript code
echo "Formatting TypeScript/JavaScript code..."
cd "$PROJECT_ROOT/web-ui" && npm run format

# Format C++ code
echo "Formatting C++ code..."
find "$PROJECT_ROOT" -type f \( -name "*.cpp" -o -name "*.h" -o -name "*.hpp" \) -exec clang-format -i {} \;

echo "Code formatting complete!"
