#!/bin/bash

echo "🎨 Starting HoloDoodle Pro Frontend..."
cd frontend

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Start dev server
echo "🔥 Starting React dev server on http://localhost:3000"
npm run dev

