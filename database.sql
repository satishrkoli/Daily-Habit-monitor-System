-- =========================================================
-- DAILY HABIT MONITORING SYSTEM - DATABASE SCHEMA SCRIPT
-- Database Engine: MySQL 8.0
-- =========================================================

-- Step 1: Create Database
CREATE DATABASE IF NOT EXISTS daily_habit_db;
USE daily_habit_db;

-- Step 2: Table 1 - users
CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL
);

-- Step 3: Table 2 - habits
CREATE TABLE IF NOT EXISTS habits (
    habit_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    habit_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    frequency VARCHAR(30) NOT NULL,
    target VARCHAR(100) NOT NULL,
    is_important VARCHAR(10) DEFAULT 'No',
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Step 4: Table 3 - habit_records
CREATE TABLE IF NOT EXISTS habit_records (
    record_id INT PRIMARY KEY AUTO_INCREMENT,
    habit_id INT NOT NULL,
    record_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Completed',
    FOREIGN KEY (habit_id) REFERENCES habits(habit_id) ON DELETE CASCADE
);
