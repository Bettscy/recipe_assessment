# Recipe API - Getting Started Guide

This guide will help you set up the Recipe API project on your laptop from scratch.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Initial Setup](#initial-setup)
3. [Database Setup](#database-setup)
4. [Running the Application](#running-the-application)
5. [Testing the API](#testing-the-api)
6. [Troubleshooting](#troubleshooting)
7. [Project Structure](#project-structure)

---

## 📦 Prerequisites

Before starting, make sure you have the following installed on your laptop:

### 1. **Python 3.8 or higher**

**Check if Python is installed:**
```bash
python3 --version
```

**If not installed:**
- **macOS**: Download from [python.org](https://www.python.org/downloads/) or use Homebrew:
  ```bash
  brew install python3
  ```
- **Windows**: Download from [python.org](https://www.python.org/downloads/)
- **Linux (Ubuntu/Debian)**:
  ```bash
  sudo apt-get update
  sudo apt-get install python3 python3-pip python3-venv
  ```

### 2. **PostgreSQL 12 or higher**

**Check if PostgreSQL is installed:**
```bash
psql --version
```

**If not installed:**

**macOS:**
```bash
# Using Homebrew
brew install postgresql@14
brew services start postgresql@14

# Add to PATH (add this to your ~/.zshrc or ~/.bash_profile)
echo 'export PATH="/opt/homebrew/opt/postgresql@14/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**Windows:**
1. Download PostgreSQL installer from [postgresql.org](https://www.postgresql.org/download/windows/)
2. Run the installer and follow the setup wizard
3. Remember the password you set for the `postgres` user

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### 3. **Git** (optional, if you received this as a zip file, skip this)

```bash
git --version
```

If not installed, download from [git-scm.com](https://git-scm.com/downloads)

---

## 🚀 Initial Setup

### Step 1: Extract the Project

If you received this as a zip file:
1. Extract `recipe_project.zip` to your desired location
2. Open Terminal (macOS/Linux) or Command Prompt (Windows)
3. Navigate to the project directory:
   ```bash
   cd path/to/recipe_project/backend
   ```

### Step 2: Create Virtual Environment

Create a Python virtual environment to isolate project dependencies:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

**You'll know it's activated when you see `(venv)` at the beginning of your terminal prompt.**

### Step 3: Install Python Dependencies

With the virtual environment activated:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install:
- Django 4.2.7
- Django REST Framework 3.14.0
- psycopg2-binary 2.9.9 (PostgreSQL adapter)
- django-filter 23.3
- python-dotenv 1.0.0

**Wait for all packages to install completely before proceeding.**

---

## 🗄️ Database Setup

### Step 1: Start PostgreSQL

**macOS:**
```bash
brew services start postgresql@14
```


- Check in Services or use pgAdmin

### Step 2: Create Database

**macOS/Linux:**
```bash
# Create database (replace 'your_username' with your system username)
createdb recipe_db

# If you get permission errors, try:
createdb -U postgres recipe_db
# You may be prompted for the postgres user password
```

**Alternative method using psql:**
```bash
# Connect to PostgreSQL
psql postgres

# Inside psql, run:
CREATE DATABASE recipe_db;

# Exit psql
\q
```

**Windows:**
```cmd
# Open Command Prompt and run:
psql -U postgres

# Inside psql:
CREATE DATABASE recipe_db;

# Exit
\q
```

### Step 3: Configure Environment Variables

Create a `.env` file in the project root (backend directory):

```bash
# Copy the example file
cp .env.example .env
```

Edit `.env` with your text editor and update the database credentials:

```env
# Django Settings
SECRET_KEY=_XWq58XXfvEGw-QpWGB9VFpdCtSqZkN6aGcmG2lx5I3gVbQVCrzRE3AIgbjKMtVr11k
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Settings
DB_NAME=recipe_db
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

**Important:**
- Replace `your_username` with your system username or `postgres`
- Replace `your_password` with your PostgreSQL password (leave blank if no password)
- On macOS, the default user is usually your system username with no password
- On Windows, it's usually `postgres` with the password you set during installation

### Step 4: Run Database Migrations

Apply Django migrations to create tables:

```bash
# Make sure your virtual environment is activated
python manage.py makemigrations
python manage.py migrate
```

You should see output showing all migrations being applied successfully.

### Step 5: Load Recipe Data

Load the recipe data from the JSON file into the database:

```bash
python manage.py load_recipes US_recipes_null.json
```

**This will take 2-3 minutes.** You'll see progress updates every 100 recipes.

Expected output:
```
Loading recipes from US_recipes_null.json...
Found 8451 recipes in JSON file
Loaded 100 recipes...
Loaded 200 recipes...
...
Successfully loaded 8244 recipes. Skipped 207 invalid entries.
```

### Step 6: Create Admin User (Optional)

If you want to access the Django admin interface:

```bash
python manage.py createsuperuser
```

Follow the prompts to create username, email, and password.

---

## 🏃 Running the Application

### Start the Development Server

```bash
# Make sure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Start server
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

**The API is now running!** 🎉

**To stop the server:** Press `Ctrl+C` in the terminal

---

## 🧪 Testing the API

### Method 1: Using curl (Command Line)

Open a new terminal window (keep the server running in the first one):

```bash
# Test 1: Get all recipes (paginated)
curl "http://localhost:8000/api/recipes?page=1&limit=5"

# Test 2: Search by rating
curl "http://localhost:8000/api/recipes/search?rating=>=4.5"

# Test 3: Search by calories and rating
curl "http://localhost:8000/api/recipes/search?calories=<=400&rating=>=4.5"

# Test 4: Search by title
curl "http://localhost:8000/api/recipes/search?title=pie"

# Test 5: Complex search
curl "http://localhost:8000/api/recipes/search?title=chicken&cuisine=southern&rating=>=4.5"
```

### Method 2: Using Web Browser

Simply open your browser and visit:
- **Recipe List**: http://localhost:8000/api/recipes
- **Search**: http://localhost:8000/api/recipes/search?rating=>=4.5
- **Admin Panel** (if you created superuser): http://localhost:8000/admin/

### Method 3: Using the Test Script

Run the included test script:

```bash
# In a new terminal (with venv activated)
python test_api.py
```

### Method 4: Using Postman or Insomnia

1. Open Postman/Insomnia
2. Create a new GET request
3. URL: `http://localhost:8000/api/recipes?page=1&limit=10`
4. Send the request

---

## 📚 API Endpoints

### 1. Get All Recipes (Paginated)

**Endpoint:** `GET /api/recipes`

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `limit` (optional): Results per page (default: 10, max: 100)

**Example:**
```bash
GET http://localhost:8000/api/recipes?page=1&limit=10
```

**Response:**
```json
{
  "page": 1,
  "limit": 10,
  "total": 8244,
  "data": [
    {
      "id": 1,
      "title": "Sweet Potato Pie",
      "cuisine": "Southern Recipes",
      "rating": 4.8,
      "prep_time": 15,
      "cook_time": 100,
      "total_time": 115,
      "description": "...",
      "nutrients": {...},
      "serves": "8 servings",
      ...
    }
  ]
}
```

### 2. Search Recipes

**Endpoint:** `GET /api/recipes/search`

**Query Parameters:**
- `calories`: Filter by calories (supports: `<=400`, `>=200`, `<500`, `>100`, `=350`)
- `rating`: Filter by rating (supports operators)
- `total_time`: Filter by total time in minutes (supports operators)
- `title`: Partial match, case-insensitive
- `cuisine`: Partial match, case-insensitive

**Examples:**

```bash
# Low calorie, high rating recipes
GET http://localhost:8000/api/recipes/search?calories=<=400&rating=>=4.5

# Quick recipes (under 30 minutes)
GET http://localhost:8000/api/recipes/search?total_time=<=30

# Search by title
GET http://localhost:8000/api/recipes/search?title=chocolate

# Combined search
GET http://localhost:8000/api/recipes/search?title=pie&cuisine=southern&calories=<=500
```

---

## 🔧 Troubleshooting

### Issue 1: "psycopg2" installation error

**Problem:** Error installing psycopg2 on macOS

**Solution:**
```bash
brew install postgresql@14
pip install psycopg2-binary
```

### Issue 2: Database connection refused

**Problem:** `connection to server on socket "/tmp/.s.PGSQL.5432" failed`

**Solution:**
```bash
# Start PostgreSQL
brew services start postgresql@14  # macOS
sudo systemctl start postgresql    # Linux
```

### Issue 3: "Database does not exist"

**Problem:** `FATAL: database "recipe_db" does not exist`

**Solution:**
```bash
createdb recipe_db
```

### Issue 4: Permission denied (database)

**Problem:** Cannot create database

**Solution:**
```bash
# On macOS/Linux, check your PostgreSQL user
psql postgres -c "CREATE DATABASE recipe_db;"

# Or create with postgres user
createdb -U postgres recipe_db
```

### Issue 5: Port 8000 already in use

**Problem:** `Error: That port is already in use.`

**Solution:**
```bash
# Find and kill the process
lsof -ti:8000 | xargs kill -9

# Or run on different port
python manage.py runserver 8001
```

### Issue 6: Virtual environment not activating (Windows)

**Problem:** Script execution disabled

**Solution:**
```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy RemoteSigned

# Then activate
venv\Scripts\activate
```

### Issue 7: Migration errors

**Problem:** Migrations not applying

**Solution:**
```bash
# Reset migrations
python manage.py migrate recipes zero
python manage.py makemigrations recipes
python manage.py migrate
```

---

## 📁 Project Structure

```
backend/
├── manage.py                       # Django management script
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
├── US_recipes_null.json           # Recipe data (13MB)
│
├── README.md                       # Full documentation
├── SETUP_GUIDE.md                  # Quick setup guide
├── GETTING_STARTED.md             # This file
├── schema.sql                      # Database schema reference
├── setup.sh                        # Automated setup script (macOS/Linux)
├── test_api.py                     # API testing script
│
├── recipe_project/                 # Main Django project
│   ├── __init__.py
│   ├── settings.py                 # Project settings
│   ├── urls.py                     # Root URL configuration
│   ├── wsgi.py                     # WSGI config for deployment
│   └── asgi.py                     # ASGI config for async
│
└── recipes/                        # Recipe Django app
    ├── __init__.py
    ├── models.py                   # Recipe database model
    ├── serializers.py              # API serializers
    ├── views.py                    # API views/endpoints
    ├── urls.py                     # App URL routes
    ├── admin.py                    # Django admin config
    ├── apps.py                     # App configuration
    ├── migrations/                 # Database migrations
    └── management/
        └── commands/
            └── load_recipes.py     # Custom command to load data
```

---

## 🎓 Next Steps

Once you have the API running:

1. **Explore the API**: Try different search combinations
2. **Check Django Admin**: Visit http://localhost:8000/admin/
3. **Read the Code**: Understand how the API works
4. **Build a Frontend**: Create a React/Vue/Angular app to consume this API
5. **Add Features**: Implement user authentication, favorites, ratings, etc.

---

## 💡 Tips

### Development Workflow

```bash
# Daily workflow

# 1. Navigate to project
cd path/to/recipe_project/backend

# 2. Activate virtual environment
source venv/bin/activate

# 3. Start server
python manage.py runserver

# 4. When done, deactivate
deactivate
```

### Useful Django Commands

```bash
# Check database status
python manage.py dbshell

# Create new migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Django shell (interactive Python with Django)
python manage.py shell

# Run tests
python manage.py test

# Check for issues
python manage.py check
```

### Database Queries

```bash
# Connect to database
psql -d recipe_db

# Useful queries:
SELECT COUNT(*) FROM recipes_recipe;
SELECT title, rating FROM recipes_recipe ORDER BY rating DESC LIMIT 10;
\dt  # List all tables
\d recipes_recipe  # Describe recipe table
\q  # Quit
```

---

## 📝 Configuration Files

### .env
Contains sensitive configuration (DO NOT share):
- Database credentials
- Secret keys
- Debug settings

### requirements.txt
Python package dependencies. To update:
```bash
pip freeze > requirements.txt
```

### .gitignore
Files to exclude from version control:
- `venv/` - Virtual environment
- `*.pyc` - Python cache
- `.env` - Environment variables
- `__pycache__/` - Python cache directories

---

## 🔒 Security Notes

1. **Never commit `.env` file** to version control
2. **Change SECRET_KEY** before deploying to production
3. **Set DEBUG=False** in production
4. **Use strong database passwords** in production
5. **Keep dependencies updated**: `pip list --outdated`

---

## 🤝 Support

If you encounter any issues:

1. **Check this guide** for troubleshooting steps
2. **Review error messages** carefully
3. **Check Django/PostgreSQL logs**
4. **Verify all prerequisites** are installed
5. **Ensure PostgreSQL is running**
6. **Check .env configuration**

---

## 📄 License

This project is for educational/assessment purposes.

---

## 🎉 You're All Set!

If you've completed all steps successfully, you should have:
- ✅ PostgreSQL database with 8,244 recipes
- ✅ Django API server running on http://localhost:8000
- ✅ Two working endpoints: `/api/recipes` and `/api/recipes/search`
- ✅ Ability to filter recipes by rating, calories, time, title, and cuisine

**Enjoy exploring the Recipe API!** 🚀
