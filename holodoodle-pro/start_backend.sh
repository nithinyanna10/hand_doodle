#!/bin/bash

echo "🚀 Starting HoloDoodle Pro Backend..."
cd backend

# Create venv if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Start server
echo "🔥 Starting FastAPI server on http://localhost:8000"
python app.py

