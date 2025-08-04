-- SQL script to generate the HBnB database schema and populate with initial data

-- Create User Table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    is_admin BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create Amenity Table
CREATE TABLE IF NOT EXISTS amenities (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create Place Table
CREATE TABLE IF NOT EXISTS places (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255),
    description TEXT,
    price DECIMAL(10, 2),
    latitude FLOAT,
    longitude FLOAT,
    owner_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(id)
);

-- Create Review Table
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    user_id INTEGER,
    place_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (place_id) REFERENCES places(id),
    UNIQUE (user_id, place_id)
);

-- Create Place_Amenity Table (Many-to-Many)
CREATE TABLE IF NOT EXISTS place_amenity (
    place_id INTEGER,
    amenity_id CHAR(36),
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES places(id),
    FOREIGN KEY (amenity_id) REFERENCES amenities(id)
);

-- Insert Initial Data

-- Admin User
INSERT INTO users (first_name, last_name, email, password, is_admin) VALUES
('Admin', 'HBnB', 'admin@hbnb.io', '$2b$12$vNMF/q2fOrBTKre68jKOzuEtrChJb1cjQWmwlFUa.axtijq2/Fski', TRUE);

-- Regular User
INSERT INTO users (first_name, last_name, email, password, is_admin) VALUES
('John', 'Doe', 'john.doe@example.com', '$2b$12$vNMF/q2fOrBTKre68jKOzuEtrChJb1cjQWmwlFUa.axtijq2/Fski', FALSE);

-- Initial Amenities
INSERT INTO amenities (id, name) VALUES
('a1b2c3d4-e5f6-7890-1234-567890abcdef', 'WiFi'),
('b2c3d4e5-f6a7-8901-2345-67890abcdef0', 'Swimming Pool'),
('c3d4e5f6-a7b8-9012-3456-7890abcdef01', 'Air Conditioning');

-- Sample Places
INSERT INTO places (title, description, price, latitude, longitude, owner_id) VALUES
('Cozy Apartment', 'A beautiful apartment in the city center.', 120.00, 34.0522, -118.2437, (SELECT id FROM users WHERE email = 'john.doe@example.com')),
('Spacious Villa', 'Luxury villa with a private pool.', 300.00, 34.0522, -118.2437, (SELECT id FROM users WHERE email = 'john.doe@example.com'));