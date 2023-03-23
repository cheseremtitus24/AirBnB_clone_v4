-- creates the specified database only when it
-- does not exist
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- Query creates a database users
-- hbnb_dev
-- Handles error when user already exists
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';
-- Query Grants all privileges on the hbnb_dev_db to user hbnb_dev
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';
-- Grant Select Permission on all Tables within performance_schema to same user
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';
