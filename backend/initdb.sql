BEGIN;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT,
    mobileno TEXT,
    isadmin BOOLEAN DEFAULT 0
);

-- Create category table
CREATE TABLE IF NOT EXISTS category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

-- Create books table
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    desc TEXT,
    author TEXT,
    category INTEGER,
    price INTEGER,
    FOREIGN KEY (category) REFERENCES category (id)
);

-- Create borrow table
CREATE TABLE IF NOT EXISTS borrow (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    userid INTEGER,
    bookid INTEGER,
    borrowedat DATE DEFAULT CURRENT_TIMESTAMP,
    returnat DATE,
    isreturned BOOLEAN DEFAULT 0,
    FOREIGN KEY (userid) REFERENCES users (id),
    FOREIGN KEY (bookid) REFERENCES books (id)
);

COMMIT;
