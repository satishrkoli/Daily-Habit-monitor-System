"""
===================================================================
DAILY HABIT MONITORING SYSTEM - MAIN ENTRY POINT
===================================================================
This is the starting file of the application.
It initializes the MySQL database schema automatically and launches
the Tkinter Login Screen.

Run Command:
python main.py
"""

import tkinter as tk
from tkinter import messagebox
import database
from login import LoginWindow


def main():
    """Main application launcher function"""
    # Step 1: Initialize Database and Tables automatically
    success, msg = database.init_db()
    if not success:
        print(f"Warning: Database auto-initialization check failed: {msg}")
        # Note: App will still launch so user can verify GUI or database credentials

    # Step 2: Initialize Tkinter Root Window
    root = tk.Tk()

    # Step 3: Instantiate Login Screen
    app = LoginWindow(root)

    # Step 4: Run Tkinter Main Event Loop
    root.mainloop()


if __name__ == "__main__":
    main()
