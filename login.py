"""
===================================================================
DAILY HABIT MONITORING SYSTEM - LOGIN MODULE
===================================================================
This module handles the Login Screen GUI and authentication logic.

Components:
- Title Label
- Username & Password Entry widgets
- Login, Register, and Exit buttons
- MySQL credentials verification using parameterized SQL SELECT query
"""

import tkinter as tk
from tkinter import messagebox
import pymysql
import database
from registration import RegistrationWindow
from dashboard import DashboardWindow


class LoginWindow:
    def __init__(self, root):
        """Initialize the Login Screen"""
        self.root = root
        self.root.title("Daily Habit Monitoring System - Login")
        self.root.geometry("450x450")
        self.root.resizable(False, False)
        self.root.configure(bg="#2C3E50")

        self.create_widgets()

    def create_widgets(self):
        """Construct GUI widgets for Login Screen"""
        # App Title Label
        title_label = tk.Label(
            self.root,
            text="DAILY HABIT MONITORING SYSTEM",
            font=("Arial", 14, "bold"),
            bg="#2C3E50",
            fg="#ECF0F1"
        )
        title_label.pack(pady=(30, 10))

        subtitle_label = tk.Label(
            self.root,
            text="Please login to manage your daily habits",
            font=("Arial", 10, "italic"),
            bg="#2C3E50",
            fg="#BDC3C7"
        )
        subtitle_label.pack(pady=(0, 20))

        # Main Card Frame
        card_frame = tk.Frame(self.root, bg="#FFFFFF", bd=2, relief="groove")
        card_frame.pack(pady=10, padx=40, fill="both", expand=True)

        # Login Header inside Card
        tk.Label(
            card_frame,
            text="USER LOGIN",
            font=("Arial", 14, "bold"),
            bg="#FFFFFF",
            fg="#2C3E50"
        ).pack(pady=15)

        # Username Input
        tk.Label(
            card_frame,
            text="Username:",
            font=("Arial", 10, "bold"),
            bg="#FFFFFF"
        ).pack(anchor="w", padx=30, pady=(5, 0))
        
        self.username_entry = tk.Entry(card_frame, font=("Arial", 11), width=28)
        self.username_entry.pack(padx=30, pady=(0, 10), ipady=3)

        # Password Input
        tk.Label(
            card_frame,
            text="Password:",
            font=("Arial", 10, "bold"),
            bg="#FFFFFF"
        ).pack(anchor="w", padx=30, pady=(5, 0))
        
        self.password_entry = tk.Entry(card_frame, font=("Arial", 11), show="*", width=28)
        self.password_entry.pack(padx=30, pady=(0, 15), ipady=3)

        # Buttons Frame
        btn_frame = tk.Frame(card_frame, bg="#FFFFFF")
        btn_frame.pack(pady=10)

        # Login Button
        login_btn = tk.Button(
            btn_frame,
            text="Login",
            font=("Arial", 10, "bold"),
            bg="#2980B9",
            fg="white",
            width=10,
            cursor="hand2",
            command=self.login
        )
        login_btn.grid(row=0, column=0, padx=5)

        # Register Button
        register_btn = tk.Button(
            btn_frame,
            text="Register",
            font=("Arial", 10, "bold"),
            bg="#27AE60",
            fg="white",
            width=10,
            cursor="hand2",
            command=self.open_registration
        )
        register_btn.grid(row=0, column=1, padx=5)

        # Exit Button
        exit_btn = tk.Button(
            btn_frame,
            text="Exit",
            font=("Arial", 10, "bold"),
            bg="#C0392B",
            fg="white",
            width=8,
            cursor="hand2",
            command=self.exit_app
        )
        exit_btn.grid(row=0, column=2, padx=5)

    def login(self):
        """
        Authenticates credentials against MySQL users table.
        Demonstrates Exception Handling, Parameterized Queries, and Log File Handling.
        """
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        # Validation: Check empty inputs
        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter both username and password.")
            return

        conn = None
        try:
            conn = database.get_connection()
            cursor = conn.cursor()

            # SQL SELECT Query using Parameterized %s
            query = """
                SELECT user_id, name, username, email
                FROM users
                WHERE username = %s AND password = %s
            """
            cursor.execute(query, (username, password))
            
            # Python Concept: TUPLE fetch result
            result = cursor.fetchone()
            cursor.close()

            if result:
                # User authenticated successfully
                # Python Concept: DICTIONARY user context
                user_data = {
                    "user_id": result[0],
                    "name": result[1],
                    "username": result[2],
                    "email": result[3]
                }

                database.log_action("LOGIN_SUCCESS", f"User logged in: {username}")
                messagebox.showinfo("Success", f"Welcome back, {user_data['name']}!")

                # Clear login entries
                self.username_entry.delete(0, tk.END)
                self.password_entry.delete(0, tk.END)

                # Hide login window and open Dashboard
                self.root.withdraw()
                DashboardWindow(self.root, user_data)

            else:
                # Authentication failed
                database.log_action("LOGIN_FAILED", f"Invalid login attempt for username: {username}")
                messagebox.showerror("Login Error", "Invalid username or password. Please try again.")

        except pymysql.MySQLError as e:
            database.log_action("DATABASE_ERROR", f"Login DB Error: {e}")
            messagebox.showerror("Database Error", f"Unable to connect to database:\n{e}")
        finally:
            if conn:
                conn.close()

    def open_registration(self):
        """Opens Registration Toplevel Window"""
        self.root.withdraw()
        RegistrationWindow(self.root, on_back_callback=self.show_login)

    def show_login(self):
        """Restores the Login window view"""
        self.root.deiconify()

    def exit_app(self):
        """Exits the application cleanly"""
        database.log_action("SYSTEM", "Application closed by user from Login Screen.")
        self.root.destroy()
