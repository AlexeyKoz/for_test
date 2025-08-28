-- Database initialization script
-- This file will be executed when the PostgreSQL container starts for the first time

-- Create additional database extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create database if it doesn't exist (PostgreSQL will automatically create the main database)
-- Additional setup can be added here

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE project_db TO postgres;

-- You can add initial data here if needed
-- Example:
-- INSERT INTO some_table (column1, column2) VALUES ('value1', 'value2');

-- Print a confirmation message
DO $$ BEGIN RAISE NOTICE 'Database initialization completed successfully!';

END $$;