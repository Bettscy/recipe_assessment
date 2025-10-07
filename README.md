# Recipe API - Django Backend

A Django REST API for managing and searching recipes with PostgreSQL database.

## Features

- Store recipe data with PostgreSQL JSONB support for flexible nutrient storage
- Paginated recipe listing sorted by rating
- Advanced search with operator support (<=, >=, <, >, =)
- Search by calories, title, cuisine, total_time, and rating
- RESTful API endpoints
- Django Admin interface for data management

## Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)

## Database Setup

1. **Install PostgreSQL** (if not already installed)
   ```bash
   # macOS
   brew install postgresql
   brew services start postgresql

   # Ubuntu/Debian
   sudo apt-get install postgresql postgresql-contrib
   sudo systemctl start postgresql
   ```

2. **Create Database**
   ```bash
   # Login to PostgreSQL
   psql postgres

   # Create database and user
   CREATE DATABASE recipe_db;
   CREATE USER postgres WITH PASSWORD 'postgres';
   GRANT ALL PRIVILEGES ON DATABASE recipe_db TO postgres;
   \q
   ```

## Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd /Users/yogesh/Downloads/recipe_project/backend
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser (optional, for Django Admin)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Load recipe data**
   ```bash
   python manage.py load_recipes n.json
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000`

## Database Schema

```sql
CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    cuisine VARCHAR(255),
    title VARCHAR(500) NOT NULL,
    rating FLOAT,
    prep_time INTEGER,
    cook_time INTEGER,
    total_time INTEGER,
    description TEXT,
    serves VARCHAR(100),
    nutrients JSONB,
    continent VARCHAR(255),
    country_state VARCHAR(255),
    url VARCHAR(1000),
    ingredients JSONB,
    instructions JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_recipes_rating ON recipes(rating DESC);
CREATE INDEX idx_recipes_cuisine ON recipes(cuisine);
CREATE INDEX idx_recipes_total_time ON recipes(total_time);
```

## API Endpoints

### 1. Get All Recipes (Paginated)

**Endpoint:** `GET /api/recipes`

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `limit` (optional): Number of results per page (default: 10, max: 100)

**Example Request:**
```bash
curl "http://localhost:8000/api/recipes?page=1&limit=10"
```

**Example Response:**
```json
{
  "page": 1,
  "limit": 10,
  "total": 50,
  "data": [
    {
      "id": 1,
      "title": "Sweet Potato Pie",
      "cuisine": "Southern Recipes",
      "rating": 4.8,
      "prep_time": 15,
      "cook_time": 100,
      "total_time": 115,
      "description": "Shared from a Southern recipe...",
      "nutrients": {
        "calories": "389 kcal",
        "carbohydrateContent": "48 g",
        "proteinContent": "5 g",
        "fatContent": "21 g"
      },
      "serves": "8 servings",
      "continent": "North America",
      "country_state": "US",
      "url": "https://www.allrecipes.com/recipe/12142/sweet-potato-pie-i/",
      "ingredients": [...],
      "instructions": [...],
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### 2. Search Recipes

**Endpoint:** `GET /api/recipes/search`

**Query Parameters:**
- `calories`: Filter by calories (supports operators: <=, >=, <, >, =)
- `title`: Filter by title (partial match, case-insensitive)
- `cuisine`: Filter by cuisine (partial match, case-insensitive)
- `total_time`: Filter by total time in minutes (supports operators)
- `rating`: Filter by rating (supports operators)

**Example Requests:**

1. Search by calories and rating:
```bash
curl "http://localhost:8000/api/recipes/search?calories=<=400&rating=>=4.5"
```

2. Search by title:
```bash
curl "http://localhost:8000/api/recipes/search?title=pie"
```

3. Search by cuisine and total time:
```bash
curl "http://localhost:8000/api/recipes/search?cuisine=Southern&total_time=<=120"
```

4. Combined search:
```bash
curl "http://localhost:8000/api/recipes/search?calories=<=400&title=pie&rating=>=4.5&cuisine=Southern"
```

**Example Response:**
```json
{
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
      "serves": "8 servings"
    }
  ]
}
```

## Testing the API

### Using curl

```bash
# Get first page of recipes
curl http://localhost:8000/api/recipes

# Get second page with 20 results
curl "http://localhost:8000/api/recipes?page=2&limit=20"

# Search for high-rated, low-calorie recipes
curl "http://localhost:8000/api/recipes/search?calories=<=400&rating=>=4.5"

# Search for pie recipes
curl "http://localhost:8000/api/recipes/search?title=pie"
```

### Using Python requests

```python
import requests

# Get recipes
response = requests.get('http://localhost:8000/api/recipes?page=1&limit=10')
data = response.json()
print(f"Total recipes: {data['total']}")
print(f"Recipes on this page: {len(data['data'])}")

# Search recipes
response = requests.get('http://localhost:8000/api/recipes/search', params={
    'calories': '<=400',
    'rating': '>=4.5',
    'title': 'pie'
})
results = response.json()
print(f"Found {len(results['data'])} matching recipes")
```

### Using Postman or similar tools

1. **GET** `http://localhost:8000/api/recipes?page=1&limit=10`
2. **GET** `http://localhost:8000/api/recipes/search?calories=<=400&rating=>=4.5`

## Django Admin

Access the Django admin interface at `http://localhost:8000/admin/`

Use the superuser credentials created during setup.

## Project Structure

```
backend/
├── manage.py
├── requirements.txt
├── README.md
├── .env.example
├── n.json                          # Recipe data file
├── recipe_project/
│   ├── __init__.py
│   ├── settings.py                 # Django settings
│   ├── urls.py                     # Main URL configuration
│   ├── wsgi.py
│   └── asgi.py
└── recipes/
    ├── __init__.py
    ├── models.py                   # Recipe model
    ├── serializers.py              # DRF serializers
    ├── views.py                    # API views
    ├── urls.py                     # Recipe app URLs
    ├── admin.py                    # Django admin config
    ├── apps.py
    └── management/
        └── commands/
            └── load_recipes.py     # Data loading command
```

## Environment Variables

Create a `.env` file based on `.env.example`:

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

## Notes

- NaN values in the JSON are automatically converted to NULL in the database
- Recipes are sorted by rating (descending) by default
- The nutrients field uses PostgreSQL JSONB for efficient querying
- Calories are extracted from the nutrients JSONB field for filtering
- All text searches are case-insensitive

## Troubleshooting

### Database connection errors

1. Ensure PostgreSQL is running:
   ```bash
   # macOS
   brew services list

   # Linux
   sudo systemctl status postgresql
   ```

2. Verify database credentials in `.env` file

3. Test PostgreSQL connection:
   ```bash
   psql -U postgres -d recipe_db -h localhost
   ```

### Migration errors

```bash
# Reset migrations (WARNING: This will delete all data)
python manage.py migrate recipes zero
python manage.py migrate
```

### Loading data errors

Ensure the `n.json` file exists in the backend directory:
```bash
ls -l n.json
```

## License

This project is created for assessment purposes.
