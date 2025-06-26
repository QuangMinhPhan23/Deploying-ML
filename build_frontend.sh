#!/bin/bash

# Show directory contents for debugging
echo "Contents of current directory:"
ls -la

# Check if frontend directory exists
if [ ! -d "frontend" ]; then
  echo "Frontend directory not found!"
  exit 1
fi

# Check frontend directory contents
echo "Contents of frontend directory:"
ls -la frontend

# Check if package.json exists
if [ ! -f "frontend/package.json" ]; then
  echo "frontend/package.json not found!"
  exit 1
fi

# Build the frontend
cd frontend
npm install
npm run build

# Check if build was successful
if [ ! -d "build" ]; then
  echo "Build directory not created!"
  exit 1
fi

echo "Frontend build completed successfully"
