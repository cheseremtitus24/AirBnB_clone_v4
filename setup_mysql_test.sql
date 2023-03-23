-- creates the specified database only when it
-- does not exist
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- Query creates a database users
-- hbnb_test
-- Handles error when user already exists
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';
-- Query Grants all privileges on the hbnb_test_db to user hbnb_test
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';
-- Grant Select Permission on all Tables within performance_schema to same user
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';
