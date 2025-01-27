#!/bin/bash

# Check Python code formatting
echo "Checking Python code formatting..."
if ! black --check zia_benchmark/src/zia_benchmark; then
    echo "Python code is not properly formatted!"
    echo "Please run './devel/format_code.sh' to format the code"
    exit 1
fi

# Check TypeScript/JavaScript code formatting
echo "Checking TypeScript/JavaScript code formatting..."
cd web-ui
if ! npm run format:check; then
    echo "TypeScript/JavaScript code is not properly formatted!"
    echo "Please run './devel/format_code.sh' to format the code"
    exit 1
fi

echo "All code is properly formatted!"
exit 0
