-- =========================================================
-- Student Management System Database Schema Specification
-- Target DBMS: SQLite / MySQL 8.0+ / PostgreSQL 14+
-- =========================================================

-- Disable foreign key constraints during table creation
PRAGMA foreign_keys = OFF;

-- ---------------------------------------------------------
-- Table Structure: users
-- Description: Stores authentication credentials & role definitions
-- ---------------------------------------------------------
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(256) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'Staff', -- 'Admin', 'Staff'
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);

-- ---------------------------------------------------------
-- Table Structure: students
-- Description: Stores primary academic and demographic records
-- ---------------------------------------------------------
DROP TABLE IF EXISTS students;

CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usn VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    semester INTEGER NOT NULL CHECK (semester BETWEEN 1 AND 8),
    dob DATE NOT NULL,
    gender VARCHAR(10) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL,
    address TEXT NOT NULL,
    photo_filename VARCHAR(255) DEFAULT 'default_avatar.png',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_students_usn ON students(usn);
CREATE INDEX idx_students_name ON students(name);
CREATE INDEX idx_students_department ON students(department);
CREATE INDEX idx_students_email ON students(email);

PRAGMA foreign_keys = ON;
