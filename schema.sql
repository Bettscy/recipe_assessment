-- PostgreSQL Database Schema for Recipe API

-- Create database (run as postgres superuser)
-- CREATE DATABASE recipe_db;
-- \c recipe_db

-- Drop table if exists (for clean setup)
-- DROP TABLE IF EXISTS recipes CASCADE;

-- Create recipes table
CREATE TABLE IF NOT EXISTS recipes (
    id SERIAL PRIMARY KEY,

    -- Required fields from specification
    cuisine VARCHAR(255),
    title VARCHAR(500) NOT NULL,
    rating FLOAT,
    prep_time INTEGER,
    cook_time INTEGER,
    total_time INTEGER,
    description TEXT,
    serves VARCHAR(100),
    nutrients JSONB,

    -- Additional fields from JSON data
    continent VARCHAR(255),
    country_state VARCHAR(255),
    url VARCHAR(1000),
    ingredients JSONB,
    instructions JSONB,

    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_recipes_rating ON recipes(rating DESC NULLS LAST);
CREATE INDEX IF NOT EXISTS idx_recipes_cuisine ON recipes(cuisine);
CREATE INDEX IF NOT EXISTS idx_recipes_total_time ON recipes(total_time);
CREATE INDEX IF NOT EXISTS idx_recipes_title ON recipes USING gin(to_tsvector('english', title));

-- Create index on JSONB nutrients field for calories lookup
CREATE INDEX IF NOT EXISTS idx_recipes_nutrients ON recipes USING gin(nutrients);

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger to automatically update updated_at
CREATE TRIGGER update_recipes_updated_at
    BEFORE UPDATE ON recipes
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Sample query to verify schema
-- SELECT column_name, data_type, is_nullable
-- FROM information_schema.columns
-- WHERE table_name = 'recipes'
-- ORDER BY ordinal_position;

-- Sample queries for testing

-- Get all recipes sorted by rating
-- SELECT id, title, cuisine, rating, total_time
-- FROM recipes
-- ORDER BY rating DESC NULLS LAST, title
-- LIMIT 10;

-- Search recipes by calories (from JSONB)
-- SELECT id, title, rating, nutrients->>'calories' as calories
-- FROM recipes
-- WHERE CAST(REPLACE(nutrients->>'calories', ' kcal', '') AS FLOAT) <= 400
-- ORDER BY rating DESC;

-- Search with multiple filters
-- SELECT id, title, cuisine, rating, total_time, nutrients->>'calories' as calories
-- FROM recipes
-- WHERE cuisine ILIKE '%southern%'
--   AND rating >= 4.5
--   AND total_time <= 120
--   AND CAST(REPLACE(nutrients->>'calories', ' kcal', '') AS FLOAT) <= 400
-- ORDER BY rating DESC, title;

-- Count recipes by cuisine
-- SELECT cuisine, COUNT(*) as recipe_count
-- FROM recipes
-- WHERE cuisine IS NOT NULL
-- GROUP BY cuisine
-- ORDER BY recipe_count DESC
-- LIMIT 10;
