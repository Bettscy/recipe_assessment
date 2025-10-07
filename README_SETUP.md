# Recipe API Project - Setup Instructions

👋 **This project contains a complete Recipe API built with Django and PostgreSQL.**

## 📦 What's Inside

The `recipe_api_project.zip` file contains:

- ✅ Complete Django REST API project
- ✅ Recipe database model with PostgreSQL JSONB support
- ✅ 8,244+ US recipes in JSON format (13MB data file)
- ✅ API endpoints for listing and searching recipes
- ✅ Comprehensive setup guides and documentation
- ✅ Test scripts and utilities

## 🚀 Quick Start

### 1. Extract the Zip File

```bash
# Extract the zip file
unzip recipe_api_project.zip

# Navigate to the project
cd backend
```

### 2. Follow the Setup Guide

**Start here:** Open `GETTING_STARTED.md` - This is your complete step-by-step guide!

The guide covers:
- Installing prerequisites (Python, PostgreSQL)
- Setting up the virtual environment
- Configuring the database
- Loading recipe data
- Running the API server
- Testing the endpoints

### 3. Quick Setup Commands (macOS/Linux)

If you already have Python 3.8+ and PostgreSQL installed:

```bash
# Navigate to project
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create database
createdb recipe_db

# Configure environment
cp .env.example .env
# Edit .env with your database credentials

# Run migrations
python manage.py migrate

# Load recipe data
python manage.py load_recipes US_recipes_null.json

# Start server
python manage.py runserver
```

Visit: http://localhost:8000/api/recipes

## 📚 Documentation Files

- **`GETTING_STARTED.md`** ⭐ - Complete setup guide (START HERE!)
- **`README.md`** - Full project documentation and API reference
- **`SETUP_GUIDE.md`** - Quick reference guide
- **`schema.sql`** - Database schema reference

## 🔑 Key Files

```
backend/
├── GETTING_STARTED.md          ⭐ READ THIS FIRST
├── README.md                   📖 Full documentation
├── US_recipes_null.json        📊 Recipe data (8,244 recipes)
├── manage.py                   🎯 Django management script
├── requirements.txt            📦 Python dependencies
├── setup.sh                    🚀 Automated setup script
├── test_api.py                 🧪 API testing script
├── recipe_project/             Django project
└── recipes/                    Django app
```

## 🎯 What You'll Get

After setup, you'll have a fully functional REST API with:

### API Endpoints

1. **GET /api/recipes** - List all recipes (paginated, sorted by rating)
   ```
   http://localhost:8000/api/recipes?page=1&limit=10
   ```

2. **GET /api/recipes/search** - Search with filters
   ```
   http://localhost:8000/api/recipes/search?calories=<=400&rating=>=4.5
   ```

### Search Filters

- **calories**: `<=400`, `>=200`, `<500`, `>100`, `=350`
- **rating**: `>=4.5`, `<=5.0`, etc.
- **total_time**: `<=60` (minutes)
- **title**: `pie`, `chicken`, etc. (partial match)
- **cuisine**: `southern`, `italian`, etc. (partial match)

### Example Searches

```bash
# Low-calorie, high-rated recipes
curl "http://localhost:8000/api/recipes/search?calories=<=400&rating=>=4.5"

# Quick Southern recipes
curl "http://localhost:8000/api/recipes/search?cuisine=southern&total_time=<=30"

# Pie recipes
curl "http://localhost:8000/api/recipes/search?title=pie"
```

## ⚙️ System Requirements

- **Python**: 3.8 or higher
- **PostgreSQL**: 12 or higher
- **Operating System**: macOS, Linux, or Windows
- **Disk Space**: ~100MB (after installation)
- **RAM**: 2GB minimum

## 🆘 Need Help?

### If you get stuck:

1. **Read `GETTING_STARTED.md`** - It has detailed troubleshooting
2. **Check Prerequisites** - Make sure Python and PostgreSQL are installed
3. **Verify PostgreSQL is running**:
   ```bash
   # macOS
   brew services list

   # Linux
   sudo systemctl status postgresql
   ```
4. **Check the .env file** - Make sure database credentials are correct

### Common Issues:

**Can't install packages?**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Database connection error?**
```bash
# Start PostgreSQL
brew services start postgresql@14  # macOS
sudo systemctl start postgresql    # Linux
```

**Port 8000 in use?**
```bash
python manage.py runserver 8001
```

## 📖 Learning Resources

After you get it running, you can:
- Explore the code in `recipes/models.py` (database model)
- Check `recipes/views.py` (API endpoints)
- Read `recipes/serializers.py` (data formatting)
- Try modifying the API or adding features

## 🎓 What's Next?

Once the API is running:

1. **Test the endpoints** using curl, Postman, or your browser
2. **Explore Django Admin** at http://localhost:8000/admin/
3. **Build a frontend** - Create a React/Vue app to display recipes
4. **Add features** - User authentication, favorites, recipe ratings
5. **Deploy it** - Put it on a server for others to use

## 💡 Tips

- **Keep the virtual environment activated** while working
- **Use the test script**: `python test_api.py`
- **Read error messages carefully** - they usually tell you what's wrong
- **Check the terminal** where the server is running for logs

## 🙏 Final Notes

This project includes:
- ✅ Clean, production-ready code
- ✅ Comprehensive documentation
- ✅ Real recipe data (8,244+ recipes)
- ✅ RESTful API design
- ✅ PostgreSQL with JSONB support
- ✅ Pagination and advanced search
- ✅ No unnecessary files or dependencies

**Everything you need is in this package!**

---

## 🚀 Ready to Start?

1. Extract the zip file
2. Open `backend/GETTING_STARTED.md`
3. Follow the step-by-step instructions
4. Within 15-20 minutes, your API will be running!

**Good luck and have fun! 🎉**

---

*If you have any questions, all the answers are in the documentation files. Read them carefully!*
