#!/bin/bash

# Recipe API Setup Script

echo "=========================================="
echo "Recipe API - Django Backend Setup"
echo "=========================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 is installed"

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "Warning: PostgreSQL is not found. Please install PostgreSQL 12 or higher."
    echo "macOS: brew install postgresql"
    echo "Ubuntu: sudo apt-get install postgresql"
    exit 1
fi

echo "✓ PostgreSQL is installed"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

echo "✓ Virtual environment created"

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✓ Dependencies installed"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file..."
    cp .env.example .env
    echo "✓ .env file created. Please edit it with your database credentials."
else
    echo ""
    echo "✓ .env file already exists"
fi

# Check if database exists
echo ""
echo "Checking database connection..."
DB_EXISTS=$(psql -U postgres -lqt | cut -d \| -f 1 | grep -w recipe_db | wc -l)

if [ $DB_EXISTS -eq 0 ]; then
    echo "Database 'recipe_db' does not exist."
    read -p "Do you want to create it now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        createdb -U postgres recipe_db
        echo "✓ Database 'recipe_db' created"
    else
        echo "Please create the database manually:"
        echo "  createdb -U postgres recipe_db"
        exit 1
    fi
else
    echo "✓ Database 'recipe_db' exists"
fi

# Run migrations
echo ""
echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

echo "✓ Migrations completed"

# Ask to create superuser
echo ""
read -p "Do you want to create a superuser for Django admin? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python manage.py createsuperuser
fi

# Ask to load data
echo ""
if [ -f "n.json" ]; then
    read -p "Do you want to load recipe data from n.json? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Loading recipe data..."
        python manage.py load_recipes n.json
        echo "✓ Recipe data loaded"
    fi
else
    echo "Warning: n.json file not found. Please add your recipe JSON file and run:"
    echo "  python manage.py load_recipes n.json"
fi

echo ""
echo "=========================================="
echo "Setup completed successfully!"
echo "=========================================="
echo ""
echo "To start the development server:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run server: python manage.py runserver"
echo ""
echo "API will be available at: http://localhost:8000"
echo "Admin interface: http://localhost:8000/admin/"
echo ""
