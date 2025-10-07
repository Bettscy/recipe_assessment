#!/usr/bin/env python3
"""
Script to test Recipe API endpoints
"""

import requests
import json

BASE_URL = "http://localhost:8000/api"


def test_recipe_list():
    """Test GET /api/recipes endpoint"""
    print("\n" + "="*60)
    print("Testing GET /api/recipes (Paginated List)")
    print("="*60)

    # Test basic listing
    response = requests.get(f"{BASE_URL}/recipes")
    print(f"\nStatus Code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"Page: {data.get('page')}")
        print(f"Limit: {data.get('limit')}")
        print(f"Total Recipes: {data.get('total')}")
        print(f"Recipes in this page: {len(data.get('data', []))}")

        if data.get('data'):
            print("\nFirst Recipe:")
            first_recipe = data['data'][0]
            print(f"  Title: {first_recipe.get('title')}")
            print(f"  Cuisine: {first_recipe.get('cuisine')}")
            print(f"  Rating: {first_recipe.get('rating')}")
            print(f"  Total Time: {first_recipe.get('total_time')} min")
    else:
        print(f"Error: {response.text}")

    # Test with pagination
    print("\n" + "-"*60)
    print("Testing with pagination (page=2, limit=5)")
    response = requests.get(f"{BASE_URL}/recipes?page=2&limit=5")
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"Page: {data.get('page')}")
        print(f"Limit: {data.get('limit')}")
        print(f"Recipes in this page: {len(data.get('data', []))}")


def test_recipe_search():
    """Test GET /api/recipes/search endpoint"""
    print("\n" + "="*60)
    print("Testing GET /api/recipes/search (Search with Filters)")
    print("="*60)

    # Test 1: Search by title
    print("\n" + "-"*60)
    print("Test 1: Search by title='pie'")
    response = requests.get(f"{BASE_URL}/recipes/search", params={'title': 'pie'})
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"Results found: {len(data.get('data', []))}")
        if data.get('data'):
            print("\nFirst 3 results:")
            for recipe in data['data'][:3]:
                print(f"  - {recipe.get('title')} (Rating: {recipe.get('rating')})")

    # Test 2: Search by rating
    print("\n" + "-"*60)
    print("Test 2: Search by rating>=4.5")
    response = requests.get(f"{BASE_URL}/recipes/search", params={'rating': '>=4.5'})
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"Results found: {len(data.get('data', []))}")
        if data.get('data'):
            print("\nFirst 3 results:")
            for recipe in data['data'][:3]:
                print(f"  - {recipe.get('title')} (Rating: {recipe.get('rating')})")

    # Test 3: Search by calories and rating
    print("\n" + "-"*60)
    print("Test 3: Search by calories<=400 and rating>=4.5")
    response = requests.get(
        f"{BASE_URL}/recipes/search",
        params={'calories': '<=400', 'rating': '>=4.5'}
    )
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"Results found: {len(data.get('data', []))}")
        if data.get('data'):
            print("\nFirst 3 results:")
            for recipe in data['data'][:3]:
                nutrients = recipe.get('nutrients', {})
                calories = nutrients.get('calories', 'N/A') if nutrients else 'N/A'
                print(f"  - {recipe.get('title')}")
                print(f"    Rating: {recipe.get('rating')}, Calories: {calories}")

    # Test 4: Search by cuisine
    print("\n" + "-"*60)
    print("Test 4: Search by cuisine='southern'")
    response = requests.get(
        f"{BASE_URL}/recipes/search",
        params={'cuisine': 'southern'}
    )
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"Results found: {len(data.get('data', []))}")
        if data.get('data'):
            print("\nFirst 3 results:")
            for recipe in data['data'][:3]:
                print(f"  - {recipe.get('title')} (Cuisine: {recipe.get('cuisine')})")

    # Test 5: Complex search
    print("\n" + "-"*60)
    print("Test 5: Complex search (title='pie', calories<=400, rating>=4.5)")
    response = requests.get(
        f"{BASE_URL}/recipes/search",
        params={
            'title': 'pie',
            'calories': '<=400',
            'rating': '>=4.5'
        }
    )
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"Results found: {len(data.get('data', []))}")
        if data.get('data'):
            print("\nResults:")
            for recipe in data['data']:
                nutrients = recipe.get('nutrients', {})
                calories = nutrients.get('calories', 'N/A') if nutrients else 'N/A'
                print(f"  - {recipe.get('title')}")
                print(f"    Rating: {recipe.get('rating')}, Calories: {calories}")


def main():
    print("\n" + "="*60)
    print("Recipe API Test Suite")
    print("="*60)
    print(f"Base URL: {BASE_URL}")
    print("\nMake sure the Django server is running:")
    print("  python manage.py runserver")

    try:
        # Check if server is running
        response = requests.get(f"{BASE_URL}/recipes")
        if response.status_code == 404:
            print("\n❌ Server is running but endpoints not found!")
            print("Check URL configuration.")
            return
    except requests.exceptions.ConnectionError:
        print("\n❌ Cannot connect to server!")
        print("Please start the server with: python manage.py runserver")
        return

    # Run tests
    test_recipe_list()
    test_recipe_search()

    print("\n" + "="*60)
    print("Tests completed!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
