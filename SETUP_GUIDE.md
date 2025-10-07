# Recipe API - Quick Setup Guide

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

```bash
# Run the setup script
./setup.sh

# Start the server
source venv/bin/activate
python manage.py runserver
```

### Option 2: Manual Setup

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your PostgreSQL credentials

# 4. Create PostgreSQL database
createdb -U postgres recipe_db

# 5. Run migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create superuser (optional)
python manage.py createsuperuser

# 7. Load recipe data
python manage.py load_recipes n.json

# 8. Start server
python manage.py runserver
```

## 🗄️ Database Setup

### Install PostgreSQL

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

**Ubuntu/Debian:**
```bash
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**Windows:**
Download from [postgresql.org](https://www.postgresql.org/download/windows/)

### Create Database

```bash
# Option 1: Using createdb command
createdb -U postgres recipe_db

# Option 2: Using psql
psql -U postgres
CREATE DATABASE recipe_db;
\q
```

### Verify Database Connection

```bash
psql -U postgres -d recipe_db
\dt  # List tables (after migrations)
\q
```

## 📊 Load Recipe Data

After running migrations, load the JSON data:

```bash
python manage.py load_recipes n.json
```

This will:
- Parse the n.json file
- Handle NaN values (convert to NULL)
- Create Recipe records in database
- Show progress every 100 records

## 🧪 Test the API

### Using curl

```bash
# Test recipe list
curl http://localhost:8000/api/recipes

# Test search
curl "http://localhost:8000/api/recipes/search?rating=>=4.5&calories=<=400"
```

### Using Python test script

```bash
python test_api.py
```

### Using Browser

- Recipe List: http://localhost:8000/api/recipes
- Django Admin: http://localhost:8000/admin/

## 📁 Project Structure

```
backend/
├── manage.py                       # Django management script
├── requirements.txt                # Python dependencies
├── README.md                       # Full documentation
├── SETUP_GUIDE.md                 # This file
├── setup.sh                        # Automated setup script
├── test_api.py                     # API test script
├── schema.sql                      # Database schema
├── n.json                          # Recipe data (13MB)
├── .env.example                    # Environment template
├── .gitignore                      # Git ignore rules
│
├── recipe_project/                 # Main project
│   ├── settings.py                 # Django settings
│   ├── urls.py                     # Root URL config
│   ├── wsgi.py                     # WSGI config
│   └── asgi.py                     # ASGI config
│
└── recipes/                        # Recipe app
    ├── models.py                   # Recipe model
    ├── serializers.py              # DRF serializers
    ├── views.py                    # API views
    ├── urls.py                     # App URLs
    ├── admin.py                    # Admin config
    └── management/
        └── commands/
            └── load_recipes.py     # Data loader
```

## 🔧 Environment Variables

Create `.env` file from template:

```bash
cp .env.example .env
```

Edit `.env`:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=recipe_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

## 📡 API Endpoints

### 1. List All Recipes (Paginated)

```
GET /api/recipes?page=1&limit=10
```

**Response:**
```json
{
  "page": 1,
  "limit": 10,
  "total": 5000,
  "data": [...]
}
```

### 2. Search Recipes

```
GET /api/recipes/search?calories=<=400&rating=>=4.5&title=pie
```

**Supported filters:**
- `calories`: <=, >=, <, >, = (e.g., `<=400`)
- `rating`: <=, >=, <, >, = (e.g., `>=4.5`)
- `total_time`: <=, >=, <, >, = (e.g., `<=60`)
- `title`: partial match (e.g., `pie`)
- `cuisine`: partial match (e.g., `southern`)

**Response:**
```json
{
  "data": [...]
}
```

## 🐛 Troubleshooting

### Database Connection Error

```bash
# Check if PostgreSQL is running
brew services list  # macOS
sudo systemctl status postgresql  # Linux

# Start PostgreSQL
brew services start postgresql  # macOS
sudo systemctl start postgresql  # Linux
```

### ImportError: No module named 'psycopg2'

```bash
# Reinstall psycopg2
pip install --upgrade psycopg2-binary
```

### Migration Errors

```bash
# Reset migrations
python manage.py migrate recipes zero
python manage.py migrate
```

### Port Already in Use

```bash
# Run on different port
python manage.py runserver 8001
```

## ✅ Verify Installation

After setup, verify everything works:

```bash
# 1. Check database
psql -U postgres -d recipe_db -c "SELECT COUNT(*) FROM recipes;"

# 2. Check API
curl http://localhost:8000/api/recipes

# 3. Run test suite
python test_api.py
```

## 📚 Additional Commands

```bash
# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Django shell
python manage.py shell

# Clear all recipes
python manage.py shell
>>> from recipes.models import Recipe
>>> Recipe.objects.all().delete()
>>> exit()

# Reload recipes
python manage.py load_recipes n.json
```

## 🎯 Next Steps

1. ✅ Complete backend setup
2. 🔜 Build frontend (React/Vue)
3. 🔜 Deploy to production
4. 🔜 Add authentication
5. 🔜 Add recipe CRUD operations
6. 🔜 Add user favorites
7. 🔜 Add recipe recommendations

## 📞 Support

For issues:
1. Check README.md for detailed documentation
2. Review error messages carefully
3. Verify database connection
4. Check .env configuration

## 🎉 Success!

If you see recipes at http://localhost:8000/api/recipes, you're all set!

Happy coding! 🚀
