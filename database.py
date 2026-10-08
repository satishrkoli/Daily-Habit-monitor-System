"""
===================================================================
DAILY HABIT MONITORING SYSTEM - DATABASE & LOGGING MODULE
===================================================================
This module handles:
1. Centralized MySQL database connection using PyMySQL
2. Automatic creation of database 'daily_habit_db' and tables
3. Action and error logging into 'daily_habit_log.txt' using File Handling

Demonstrated Python Concepts:
- Dictionary (for DB Configuration)
- Functions with error handling
- File handling (open, write, append)
- Try-Except-Finally for database operations
"""

import pymysql
from datetime import datetime

# =================================================================
# 1. DATABASE CONFIGURATION (DICTIONARY)
# Easy-to-change MySQL configuration section
# Update the password value to match your MySQL root password
# =================================================================
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "satish123",  # <--- CHANGE THIS to your local MySQL password (e.g., satish123)
    "database": "daily_habit_db",
    "port": 3306
}

# Path to application log file
LOG_FILE_PATH = "daily_habit_log.txt"


# =================================================================
# 2. FILE HANDLING: ACTION & ERROR LOGGING
# =================================================================
def log_action(event_type, details):
    """
    Logs user actions and system errors into daily_habit_log.txt.
    Demonstrates Python File Handling using open() in append ('a') mode.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{event_type.upper()}] {details}\n"

    try:
        # Open file in append mode ('a')
        with open(LOG_FILE_PATH, "a", encoding="utf-8") as file:
            file.write(log_entry)
    except Exception as e:
        print(f"File Logging Error: {e}")


# =================================================================
# 3. MYSQL CONNECTION HELPER FUNCTION
# =================================================================
def get_connection():
    """
    Establishes and returns a connection to the MySQL database.
    Demonstrates Exception Handling (try-except).
    """
    try:
        connection = pymysql.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"],
            port=DB_CONFIG["port"],
            autocommit=True
        )
        return connection
    except pymysql.MySQLError as e:
        log_action("DATABASE_ERROR", f"Failed to connect to MySQL database: {e}")
        raise e


# =================================================================
# 4. AUTOMATIC DATABASE & TABLE INITIALIZATION
# =================================================================
def init_db():
    """
    Initializes the MySQL database 'daily_habit_db' and creates required tables:
    1. users
    2. habits
    3. habit_records
    """
    try:
        # Step A: Connect to MySQL server without selecting database
        connection = pymysql.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            port=DB_CONFIG["port"],
            autocommit=True
        )
        cursor = connection.cursor()

        # Step B: Create Database if it does not exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS daily_habit_db;")
        cursor.execute("USE daily_habit_db;")

        # Step C: Table 1 - users
        create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
            user_id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(100) NOT NULL,
            username VARCHAR(50) NOT NULL UNIQUE,
            password VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL
        );
        """
        cursor.execute(create_users_table)

        # Step D: Table 2 - habits
        create_habits_table = """
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
        """
        cursor.execute(create_habits_table)

        # Step E: Table 3 - habit_records
        create_records_table = """
        CREATE TABLE IF NOT EXISTS habit_records (
            record_id INT PRIMARY KEY AUTO_INCREMENT,
            habit_id INT NOT NULL,
            record_date DATE NOT NULL,
            status VARCHAR(20) NOT NULL DEFAULT 'Completed',
            FOREIGN KEY (habit_id) REFERENCES habits(habit_id) ON DELETE CASCADE
        );
        """
        cursor.execute(create_records_table)

        cursor.close()
        connection.close()
        log_action("SYSTEM", "Database and tables verified/created successfully.")
        return True, "Database initialization successful!"

    except pymysql.MySQLError as e:
        error_msg = f"Database setup error: {e}"
        log_action("ERROR", error_msg)
        return False, error_msg
