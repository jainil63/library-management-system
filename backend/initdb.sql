BEGIN;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL,
    mobileno TEXT,
    isadmin BOOLEAN DEFAULT 0
);

-- Create books table
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    desc TEXT,
    author TEXT,
    category TEXT,
    borrowby INTEGER DEFAULT NULL, 
    price INTEGER
);

COMMIT;
