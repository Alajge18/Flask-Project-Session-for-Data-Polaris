# ============================================================
# database.py — All Database Operations
# ============================================================
# This file handles EVERYTHING related to the SQLite database.
# It connects to the database, creates tables, and has functions
# to Create, Read, Update, and Delete (CRUD) data.
#
# Why a separate file?
#   app.py doesn't need to know SQL. It just calls functions like
#   get_all_tasks() and gets the data back. This is called
#   "separation of concerns" — each file has ONE job.
# ============================================================

import sqlite3
# sqlite3 is Python's built-in module for working with SQLite databases
# SQLite stores everything in a single file (tasks.db) — no server needed

DATABASE = "tasks.db"
# The name of our database file
# This file is created automatically when you first run the app
# All your data (users, tasks) is stored here permanently


def get_db():
    """
    Connect to the SQLite database and return the connection.
    
    Every time we want to read or write data, we need a "connection"
    — like picking up a phone to talk to the database.
    """
    conn = sqlite3.connect(DATABASE)
    # sqlite3.connect() opens (or creates) the database file
    # Returns a connection object that we use to send SQL commands

    conn.row_factory = sqlite3.Row
    # By default, SQLite returns data as tuples: (1, "Alice", "alice@example.com")
    # With Row factory, we can access columns by name: row["name"] → "Alice"
    # This makes our code much more readable

    conn.execute("PRAGMA foreign_keys = ON")
    # SQLite has foreign keys DISABLED by default (for backward compatibility)
    # This line turns them ON so that:
    #   - You can't create a task with user_id=99 if user 99 doesn't exist
    #   - The database enforces relationships between tables

    return conn


def init_db():
    """
    Create the users and tasks tables if they don't exist yet.
    
    This runs once when the app starts.
    IF NOT EXISTS means: only create the table if it's not already there.
    So running this multiple times is safe — it won't delete existing data.
    """
    conn = get_db()       # Step 1: Connect to the database
    cursor = conn.cursor() # Step 2: Create a cursor (a tool to execute SQL)

    # --- Create the USERS table ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)
    # id     → Unique number for each user, auto-increments (1, 2, 3...)
    # name   → The user's name. NOT NULL means it can't be empty.
    # email  → The user's email. NOT NULL means it can't be empty.
    # PRIMARY KEY → This column uniquely identifies each row
    # AUTOINCREMENT → SQLite automatically assigns the next number

    # --- Create the TASKS table ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL DEFAULT 'pending',
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    # title       → Task title. Required (NOT NULL).
    # description → Optional details. Can be empty (no NOT NULL).
    # status      → Current state. Defaults to 'pending' if not specified.
    # user_id     → Which user owns this task. Required.
    # FOREIGN KEY → user_id MUST match an existing id in the users table
    #               This is how we connect tasks to users

    conn.commit()  # Save the changes to the database file
    conn.close()   # Close the connection (free up resources)


# ============================================================
# USER FUNCTIONS — Create and Read users
# ============================================================

def get_all_users():
    """
    Get all users from the database.
    
    SQL: SELECT * FROM users
    Translation: "Give me ALL columns (*) FROM the users table"
    
    Returns: A list of user rows
    """
    conn = get_db()
    users = conn.execute("SELECT * FROM users").fetchall()
    # .execute() runs the SQL command
    # .fetchall() gets ALL matching rows as a list
    conn.close()
    return users


def get_user_by_id(user_id):
    """
    Get one user by their ID.
    
    SQL: SELECT * FROM users WHERE id = ?
    Translation: "Give me the user WHERE their id equals this number"
    
    The ? is a placeholder. We pass the actual value as a tuple (user_id,)
    This prevents SQL injection attacks (hackers inserting malicious SQL).
    
    Returns: One user row, or None if not found
    """
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)  # The comma after user_id makes it a tuple — Python requires this
    ).fetchone()
    # .fetchone() gets just ONE row (or None if no match)
    conn.close()
    return user


def create_user(name, email):
    """
    Insert a new user into the database.
    
    SQL: INSERT INTO users (name, email) VALUES (?, ?)
    Translation: "Add a new row to users with these name and email values"
    
    Returns: The ID of the newly created user
    """
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO users (name, email) VALUES (?, ?)",
        (name, email)  # These values replace the ? placeholders in order
    )
    conn.commit()  # IMPORTANT: commit() saves the change permanently
    # Without commit(), the INSERT would be lost when the connection closes

    user_id = cursor.lastrowid
    # lastrowid gives us the auto-generated ID of the row we just inserted
    # For example, if we have users 1 and 2, the new user gets id=3

    conn.close()
    return user_id


# ============================================================
# TASK FUNCTIONS — Full CRUD (Create, Read, Update, Delete)
# ============================================================

def get_all_tasks():
    """
    Get all tasks from the database.
    
    SQL: SELECT * FROM tasks
    Returns: A list of all task rows
    """
    conn = get_db()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return tasks


def get_task_by_id(task_id):
    """
    Get one task by its ID.
    
    SQL: SELECT * FROM tasks WHERE id = ?
    Returns: One task row, or None if not found
    """
    conn = get_db()
    task = conn.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()
    conn.close()
    return task


def get_tasks_by_status(status):
    """
    Get tasks filtered by their status.
    
    SQL: SELECT * FROM tasks WHERE status = ?
    Example: get_tasks_by_status("pending") → only pending tasks
    
    Returns: A list of matching task rows
    """
    conn = get_db()
    tasks = conn.execute(
        "SELECT * FROM tasks WHERE status = ?",
        (status,)
    ).fetchall()
    conn.close()
    return tasks


def create_task(title, description, status, user_id):
    """
    Insert a new task into the database.
    
    SQL: INSERT INTO tasks (title, description, status, user_id) VALUES (?, ?, ?, ?)
    
    Returns: The ID of the newly created task
    """
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO tasks (title, description, status, user_id) VALUES (?, ?, ?, ?)",
        (title, description, status, user_id)
    )
    conn.commit()  # Save the new task permanently
    task_id = cursor.lastrowid  # Get the auto-generated ID
    conn.close()
    return task_id


def update_task(task_id, title, description, status):
    """
    Update an existing task's title, description, and status.
    
    SQL: UPDATE tasks SET title=?, description=?, status=? WHERE id=?
    Translation: "Change these columns WHERE the id matches"
    
    Note: We don't update user_id — a task stays with its original user.
    """
    conn = get_db()
    conn.execute(
        "UPDATE tasks SET title = ?, description = ?, status = ? WHERE id = ?",
        (title, description, status, task_id)
        # The values replace ? in order: title→first ?, description→second ?, etc.
    )
    conn.commit()  # Save the changes permanently
    conn.close()


def delete_task(task_id):
    """
    Delete a task from the database.
    
    SQL: DELETE FROM tasks WHERE id = ?
    Translation: "Remove the row WHERE id matches"
    
    WARNING: This is permanent! The task cannot be recovered.
    """
    conn = get_db()
    conn.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )
    conn.commit()  # Save the deletion permanently
    conn.close()
