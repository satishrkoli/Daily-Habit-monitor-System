"""
===================================================================
DAILY HABIT MONITORING SYSTEM - REGISTRATION MODULE
===================================================================
This module provides the User Registration GUI window and registration logic.

Fields: Name, Username, Password, Email
Validation: Empty check, duplicate username error handling
"""

import tkinter as tk
from tkinter import messagebox
import pymysql
import database


class RegistrationWindow:
    def __init__(self, parent, on_back_callback):
        """
        Initialize Registration Window using Tkinter Toplevel.
        """
        self.parent = parent
        self.on_back_callback = on_back_callback

        self.window = tk.Toplevel(parent)
        self.window.title("Daily Habit System - Register")
        self.window.geometry("450x520")
        self.window.resizable(False, False)
        self.window.configure(bg="#F4F6F9")

        # Handle window close (X button)
        self.window.protocol("WM_DELETE_WINDOW", self.back_to_login)

        self.create_widgets()

    def create_widgets(self):
        """Build GUI widgets for Registration Form"""
        # Header Label
        header_label = tk.Label(
            self.window,
            text="CREATE NEW ACCOUNT",
            font=("Arial", 16, "bold"),
            bg="#F4F6F9",
            fg="#2C3E50"
        )
        header_label.pack(pady=20)

        # Form Frame
        form_frame = tk.Frame(self.window, bg="#F4F6F9")
        form_frame.pack(pady=10, padx=40, fill="both", expand=True)

        # 1. Full Name
        tk.Label(
            form_frame,
            text="Full Name:",
            font=("Arial", 10, "bold"),
            bg="#F4F6F9"
        ).grid(row=0, column=0, sticky="w", pady=5)
        self.name_entry = tk.Entry(form_frame, font=("Arial", 11), width=30)
        self.name_entry.grid(row=1, column=0, pady=5, ipady=3)

        # 2. Username
        tk.Label(
            form_frame,
            text="Username:",
            font=("Arial", 10, "bold"),
            bg="#F4F6F9"
        ).grid(row=2, column=0, sticky="w", pady=5)
        self.username_entry = tk.Entry(form_frame, font=("Arial", 11), width=30)
        self.username_entry.grid(row=3, column=0, pady=5, ipady=3)

        # 3. Password
        tk.Label(
            form_frame,
            text="Password:",
            font=("Arial", 10, "bold"),
            bg="#F4F6F9"
        ).grid(row=4, column=0, sticky="w", pady=5)
        self.password_entry = tk.Entry(form_frame, font=("Arial", 11), show="*", width=30)
        self.password_entry.grid(row=5, column=0, pady=5, ipady=3)

        # 4. Email
        tk.Label(
            form_frame,
            text="Email Address:",
            font=("Arial", 10, "bold"),
            bg="#F4F6F9"
        ).grid(row=6, column=0, sticky="w", pady=5)
        self.email_entry = tk.Entry(form_frame, font=("Arial", 11), width=30)
        self.email_entry.grid(row=7, column=0, pady=5, ipady=3)

        # Button Frame
        button_frame = tk.Frame(self.window, bg="#F4F6F9")
        button_frame.pack(pady=20)

        # Register Button
        register_btn = tk.Button(
            button_frame,
            text="Register",
            font=("Arial", 10, "bold"),
            bg="#27AE60",
            fg="white",
            width=10,
            cursor="hand2",
            command=self.register_user
        )
        register_btn.grid(row=0, column=0, padx=5)

        # Clear Button
        clear_btn = tk.Button(
            button_frame,
            text="Clear",
            font=("Arial", 10, "bold"),
            bg="#E67E22",
            fg="white",
            width=10,
            cursor="hand2",
            command=self.clear_fields
        )
        clear_btn.grid(row=0, column=1, padx=5)

        # Back Button
        back_btn = tk.Button(
            button_frame,
            text="Back to Login",
            font=("Arial", 10, "bold"),
            bg="#7F8C8D",
            fg="white",
            width=12,
            cursor="hand2",
            command=self.back_to_login
        )
        back_btn.grid(row=0, column=2, padx=5)

    def register_user(self):
        """
        Validates form entries and registers new user into MySQL database.
        Demonstrates Dictionary usage and Exception Handling.
        """
        name = self.name_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        email = self.email_entry.get().strip()

        # Requirement 2: Validation of required fields
        if not name or not username or not password or not email:
            messagebox.showwarning("Input Error", "All fields are required! Please fill in all entries.")
            return

        # Python Data Structure Concept: DICTIONARY usage
        user_data = {
            "name": name,
            "username": username,
            "password": password,
            "email": email
        }

        # Save to MySQL Database
        conn = None
        try:
            conn = database.get_connection()
            cursor = conn.cursor()

            # Parameterized Query to prevent SQL Injection
            sql_query = """
                INSERT INTO users (name, username, password, email)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(
                sql_query,
                (user_data["name"], user_data["username"], user_data["password"], user_data["email"])
            )
            cursor.close()

            # Log registration action
            database.log_action("REGISTRATION_SUCCESS", f"New user registered: {username}")

            messagebox.showinfo("Success", "Account created successfully! You can now log in.")
            self.back_to_login()

        except pymysql.err.IntegrityError:
            # Handles duplicate username error cleanly
            database.log_action("REGISTRATION_FAILED", f"Duplicate username attempted: {username}")
            messagebox.showerror("Registration Error", "Username already exists! Please choose a different username.")
        except Exception as e:
            database.log_action("REGISTRATION_ERROR", f"Error registering user: {e}")
            messagebox.showerror("Database Error", f"Failed to register account: {e}")
        finally:
            if conn:
                conn.close()

    def clear_fields(self):
        """Clears all input fields in the registration form"""
        self.name_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)

    def back_to_login(self):
        """Closes the registration window and returns to login screen"""
        self.window.destroy()
        if self.on_back_callback:
            self.on_back_callback()
