# ============================================================
# database.py — All Database Operations (Module 17, 18)
# ============================================================
# This file handles EVERYTHING related to the SQLite database.
# It connects to the database, creates tables, and has functions
# to Create, Read, Update, and Delete (CRUD) data.
#
# WHY a separate file?
#   app.py doesn't need to know SQL. It just calls functions like
#   get_all_tasks() and gets data back. This is called
#   "Separation of Concerns" — each file has ONE job.
#
# Modules Covered:
#   Module 17 — SQL Basics (CREATE, INSERT, SELECT, UPDATE, DELETE)
#   Module 18 — SQLite + Flask Integration
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

    Module 18 — SQLite Connection:
        sqlite3.connect()  → Opens (or creates) the database file
        row_factory        → Lets us access columns by NAME instead of index
    """
    conn = sqlite3.connect(DATABASE)
    # sqlite3.connect() opens (or creates) the database file
    # Returns a connection object that we use to send SQL commands

    conn.row_factory = sqlite3.Row
    # By default, SQLite returns data as tuples: (1, "Learn Flask", "...")
    # With Row factory, we can access columns by name: row["title"] → "Learn Flask"
    # This makes our code much more readable

    return conn


def init_db():
    """
    Create the users and tasks tables if they don't exist.

    This runs ONCE when the app starts.
    IF NOT EXISTS means: only create tables if they're not already there.
    So running this multiple times is safe — it won't delete existing data.

    Module 17 — SQL: CREATE TABLE
    Module 18 — Users table, Tasks table, Foreign Key relationship
    """
    conn = get_db()       # Step 1: Connect to the database
    cursor = conn.cursor() # Step 2: Create a cursor (tool to execute SQL)

    # --- Create the USERS table ---
    # Module 18: Users table with id, name, email
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # id         → Unique number for each user, auto-increments (1, 2, 3...)
    # name       → User's name. Required (NOT NULL).
    # email      → User's email. Required and UNIQUE (no duplicate emails).
    # created_at → When the user was created (auto-filled by the database)

    # --- Create the TASKS table ---
    # Module 18: Tasks table with foreign key to users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    # id          → Unique number for each task, auto-increments (1, 2, 3...)
    # user_id     → Which user this task belongs to (FOREIGN KEY to users.id)
    # title       → Task title. Required (NOT NULL).
    # description → Optional details. Can be empty (no NOT NULL).
    # status      → Current state. Defaults to 'pending' if not specified.
    # created_at  → When the task was created (auto-filled by the database)
    # FOREIGN KEY → Links user_id to users table (One-to-Many relationship)

    conn.commit()  # Save the changes to the database file
    conn.close()   # Close the connection (free up resources)


# ============================================================
# USER FUNCTIONS — Create and Read Users
# ============================================================
# Module 17 — SQL: INSERT, SELECT for users
# Module 20 — API Endpoint Design: POST /users, GET /users/<id>
# ============================================================

def create_user(name, email):
    """
    Insert a new user into the database.

    SQL: INSERT INTO users (name, email) VALUES (?, ?)
    Returns: The ID of the newly created user

    Module 17 — SQL: INSERT
    """
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO users (name, email) VALUES (?, ?)",
        (name, email)
        # The ? placeholders prevent SQL injection attacks
    )
    conn.commit()  # IMPORTANT: commit() saves the change permanently
    user_id = cursor.lastrowid  # Get the auto-generated ID
    conn.close()
    return user_id


def get_user_by_id(user_id):
    """
    Get one user by their ID.

    SQL: SELECT * FROM users WHERE id = ?
    Returns: One user row, or None if not found

    Module 17 — SQL: SELECT with WHERE
    """
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
        # The ? is a placeholder. The comma makes (user_id,) a tuple.
    ).fetchone()
    # .fetchone() gets just ONE row (or None if no match)
    conn.close()
    return user


# ============================================================
# TASK FUNCTIONS — Full CRUD (Create, Read, Update, Delete)
# ============================================================
# Module 17 — SQL: INSERT, SELECT, UPDATE, DELETE for tasks
# Module 22 — Complete CRUD operations
# ============================================================

def create_task(title, description, status, user_id=None):
    """
    Insert a new task into the database.

    SQL: INSERT INTO tasks (user_id, title, description, status) VALUES (?, ?, ?, ?)
    Returns: The ID of the newly created task

    Module 17 — SQL: INSERT
    Module 1  — Default Arguments: user_id=None
    """
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO tasks (user_id, title, description, status) VALUES (?, ?, ?, ?)",
        (user_id, title, description, status)
        # These values replace the ? placeholders in order
    )
    conn.commit()  # IMPORTANT: commit() saves the change permanently
    # Without commit(), the INSERT would be lost when the connection closes

    task_id = cursor.lastrowid
    # lastrowid gives us the auto-generated ID of the row we just inserted

    conn.close()
    return task_id


def get_all_tasks():
    """
    Get all tasks from the database, ordered by newest first.

    SQL: SELECT * FROM tasks ORDER BY id DESC
    Returns: A list of all task rows

    Module 17 — SQL: SELECT with ORDER BY
    """
    conn = get_db()
    tasks = conn.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
    # .execute() runs the SQL command
    # .fetchall() gets ALL matching rows as a list
    # ORDER BY id DESC → newest tasks appear first
    conn.close()
    return tasks


def get_task_by_id(task_id):
    """
    Get one task by its ID.

    SQL: SELECT * FROM tasks WHERE id = ?
    Returns: One task row, or None if not found

    Module 17 — SQL: SELECT with WHERE
    """
    conn = get_db()
    task = conn.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
        # The ? is a placeholder. We pass the actual value as a tuple (task_id,)
        # This prevents SQL injection attacks (hackers inserting malicious SQL).
        # The comma after task_id makes it a tuple — Python requires this
    ).fetchone()
    # .fetchone() gets just ONE row (or None if no match)
    conn.close()
    return task


def get_tasks_by_status(status):
    """
    Get tasks filtered by their status, ordered by newest first.

    SQL: SELECT * FROM tasks WHERE status = ? ORDER BY id DESC
    Example: get_tasks_by_status("pending") → only pending tasks

    Module 12 — Query Parameters: used with request.args.get("status")
    Module 17 — SQL: SELECT with WHERE
    """
    conn = get_db()
    tasks = conn.execute(
        "SELECT * FROM tasks WHERE status = ? ORDER BY id DESC",
        (status,)
    ).fetchall()
    conn.close()
    return tasks


def get_task_counts():
    """
    Get the count of tasks grouped by status.

    Returns a dictionary with:
      {"total": 10, "pending": 4, "in_progress": 3, "completed": 3}

    Module 4 — Dictionaries: returns a dictionary (used in dashboard)
    Module 17 — SQL: SELECT COUNT(*)
    """
    conn = get_db()

    total = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
    pending = conn.execute(
        "SELECT COUNT(*) FROM tasks WHERE status = 'pending'"
    ).fetchone()[0]
    in_progress = conn.execute(
        "SELECT COUNT(*) FROM tasks WHERE status = 'in_progress'"
    ).fetchone()[0]
    completed = conn.execute(
        "SELECT COUNT(*) FROM tasks WHERE status = 'completed'"
    ).fetchone()[0]

    conn.close()
    return {
        "total": total,
        "pending": pending,
        "in_progress": in_progress,
        "completed": completed
    }


def search_tasks(query, status=None):
    """
    Search tasks where title or description contains the query.
    Optionally filters by status.

    SQL: SELECT * FROM tasks WHERE (title LIKE ? OR description LIKE ?) ...
    Returns: A list of matching task rows ordered by newest first

    Module 12 — Query Parameters: used with request.args.get("q")
    Module 17 — SQL: SELECT with LIKE (pattern matching)
    """
    conn = get_db()
    pattern = f"%{query}%"
    # % means "any characters" → %Flask% matches "Learn Flask", "Flask Tutorial"

    if status and status in ("pending", "in_progress", "completed"):
        tasks = conn.execute(
            "SELECT * FROM tasks WHERE (title LIKE ? OR description LIKE ?) AND status = ? ORDER BY id DESC",
            (pattern, pattern, status)
        ).fetchall()
    else:
        tasks = conn.execute(
            "SELECT * FROM tasks WHERE (title LIKE ? OR description LIKE ?) ORDER BY id DESC",
            (pattern, pattern)
        ).fetchall()

    conn.close()
    return tasks


def update_task(task_id, title, description, status):
    """
    Update an existing task's title, description, and status.

    SQL: UPDATE tasks SET title=?, description=?, status=? WHERE id=?
    Translation: "Change these columns WHERE the id matches"

    Module 17 — SQL: UPDATE
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

    Module 17 — SQL: DELETE
    """
    conn = get_db()
    conn.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )
    conn.commit()  # Save the deletion permanently
    conn.close()
