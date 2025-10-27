#!/bin/bash

# Setup script for Adaptive Medical Learning System Backend

set -e  # Exit on error

echo "==================================="
echo "Setting up Adaptive Medical Learning System"
echo "==================================="

# Check Python version
echo ""
echo "Checking Python version..."
python3 --version

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Copy .env.example to .env if not exists
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration!"
else
    echo ""
    echo ".env file already exists."
fi

# Create upload directory
echo ""
echo "Creating upload directory..."
mkdir -p uploads

echo ""
echo "==================================="
echo "Setup complete!"
echo "==================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your configuration (database, API keys, etc.)"
echo "2. Make sure PostgreSQL is running with pgvector extension"
echo "3. Run database migrations: alembic upgrade head"
echo "4. Start the server: uvicorn app.main:app --reload"
echo ""
echo "Or use Docker:"
echo "docker-compose up -d"
echo ""
