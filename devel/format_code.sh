#!/bin/bash

# Format Python code
echo "Formatting Python code..."
black zia_benchmark/src/zia_benchmark

# Format TypeScript/JavaScript code
echo "Formatting TypeScript/JavaScript code..."
cd web-ui && npm run format

echo "Code formatting complete!"
