#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Check Python code formatting
echo "Checking Python code formatting..."
if ! black --check "$PROJECT_ROOT/benchcompress/src/benchcompress"; then
    echo "Python code is not properly formatted!"
    echo "Please run './devel/format_code.sh' to format the code"
    exit 1
fi

# Check TypeScript/JavaScript code formatting
echo "Checking TypeScript/JavaScript code formatting..."
cd "$PROJECT_ROOT/web-ui"
if ! npm run format:check; then
    echo "TypeScript/JavaScript code is not properly formatted!"
    echo "Please run './devel/format_code.sh' to format the code"
    exit 1
fi

# Check C++ code formatting
echo "Checking C++ code formatting..."
cpp_files=$(find "$PROJECT_ROOT" -type f \( -name "*.cpp" -o -name "*.h" -o -name "*.hpp" \))
for file in $cpp_files; do
    if ! clang-format --dry-run -Werror "$file" > /dev/null 2>&1; then
        echo "C++ code is not properly formatted!"
        echo "Please run './devel/format_code.sh' to format the code"
        exit 1
    fi
done

echo "All code is properly formatted!"
exit 0
