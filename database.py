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
# All your data (tasks) is stored here permanently


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
    # By default, SQLite returns data as tuples: (1, "Learn Flask", "...")
    # With Row factory, we can access columns by name: row["title"] → "Learn Flask"
    # This makes our code much more readable

    return conn


def init_db():
    """
    Create the tasks table if it doesn't exist yet.
    
    This runs once when the app starts.
    IF NOT EXISTS means: only create the table if it's not already there.
    So running this multiple times is safe — it won't delete existing data.
    """
    conn = get_db()       # Step 1: Connect to the database
    cursor = conn.cursor() # Step 2: Create a cursor (a tool to execute SQL)

    # --- Create the TASKS table ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # id          → Unique number for each task, auto-increments (1, 2, 3...)
    # title       → Task title. Required (NOT NULL).
    # description → Optional details. Can be empty (no NOT NULL).
    # status      → Current state. Defaults to 'pending' if not specified.
    # created_at  → When the task was created (auto-filled by the database)

    conn.commit()  # Save the changes to the database file
    conn.close()   # Close the connection (free up resources)


# ============================================================
# TASK FUNCTIONS — Full CRUD (Create, Read, Update, Delete)
# ============================================================

def get_all_tasks():
    """
    Get all tasks from the database, ordered by newest first.
    
    SQL: SELECT * FROM tasks ORDER BY id DESC
    Returns: A list of all task rows
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
    
    Returns: A list of matching task rows
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
    """
    conn = get_db()
    pattern = f"%{query}%"

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


def create_task(title, description, status):
    """
    Insert a new task into the database.
    
    SQL: INSERT INTO tasks (title, description, status) VALUES (?, ?, ?)
    
    Returns: The ID of the newly created task
    """
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO tasks (title, description, status) VALUES (?, ?, ?)",
        (title, description, status)
        # These values replace the ? placeholders in order
    )
    conn.commit()  # IMPORTANT: commit() saves the change permanently
    # Without commit(), the INSERT would be lost when the connection closes

    task_id = cursor.lastrowid
    # lastrowid gives us the auto-generated ID of the row we just inserted

    conn.close()
    return task_id


def update_task(task_id, title, description, status):
    """
    Update an existing task's title, description, and status.
    
    SQL: UPDATE tasks SET title=?, description=?, status=? WHERE id=?
    Translation: "Change these columns WHERE the id matches"
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
