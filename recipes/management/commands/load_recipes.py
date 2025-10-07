import json
import math
from django.core.management.base import BaseCommand
from recipes.models import Recipe


class Command(BaseCommand):
    help = 'Load recipes from JSON file into database'

    def add_arguments(self, parser):
        parser.add_argument(
            'json_file',
            type=str,
            help='Path to JSON file containing recipes'
        )

    def handle(self, *args, **options):
        json_file = options['json_file']

        self.stdout.write(self.style.SUCCESS(f'Loading recipes from {json_file}...'))

        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                recipes_data = json.load(f)

            self.stdout.write(f'Found {len(recipes_data)} recipes in JSON file')

            # Clear existing recipes (optional - comment out if you want to keep existing data)
            # Recipe.objects.all().delete()
            # self.stdout.write(self.style.WARNING('Cleared existing recipes'))

            created_count = 0
            skipped_count = 0

            # Handle both list and dict formats
            if isinstance(recipes_data, dict):
                recipes_list = recipes_data.values()
            else:
                recipes_list = recipes_data

            for recipe_data in recipes_list:
                # Extract and clean data
                title = recipe_data.get('title')
                if title:
                    title = title.strip()

                if not title:
                    skipped_count += 1
                    continue

                # Handle NaN values by converting to None
                def clean_numeric(value):
                    if value is None or (isinstance(value, float) and math.isnan(value)):
                        return None
                    try:
                        return float(value) if isinstance(value, (int, float, str)) else None
                    except (ValueError, TypeError):
                        return None

                def clean_int(value):
                    if value is None or (isinstance(value, float) and math.isnan(value)):
                        return None
                    try:
                        return int(float(value)) if isinstance(value, (int, float, str)) else None
                    except (ValueError, TypeError):
                        return None

                # Create recipe object
                recipe = Recipe(
                    title=title,
                    cuisine=recipe_data.get('cuisine'),
                    rating=clean_numeric(recipe_data.get('rating')),
                    prep_time=clean_int(recipe_data.get('prep_time')),
                    cook_time=clean_int(recipe_data.get('cook_time')),
                    total_time=clean_int(recipe_data.get('total_time')),
                    description=recipe_data.get('description'),
                    serves=recipe_data.get('serves'),
                    nutrients=recipe_data.get('nutrients'),
                    continent=recipe_data.get('Contient'),  # Note: typo in original JSON
                    country_state=recipe_data.get('Country_State'),
                    url=recipe_data.get('URL'),
                    ingredients=recipe_data.get('ingredients'),
                    instructions=recipe_data.get('instructions'),
                )

                recipe.save()
                created_count += 1

                if created_count % 100 == 0:
                    self.stdout.write(f'Loaded {created_count} recipes...')

            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully loaded {created_count} recipes. Skipped {skipped_count} invalid entries.'
                )
            )

        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'File not found: {json_file}')
            )
        except json.JSONDecodeError as e:
            self.stdout.write(
                self.style.ERROR(f'Invalid JSON file: {e}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error loading recipes: {e}')
            )
