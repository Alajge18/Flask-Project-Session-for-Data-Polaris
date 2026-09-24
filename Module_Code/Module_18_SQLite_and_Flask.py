"""
=============================================================================
MODULE 18: SQLite and Flask Integration
Project Story: Building our "Task Manager" Database (Step 8)
=============================================================================
Previously in Module 17:
We learned raw SQL commands (INSERT, SELECT, UPDATE, DELETE).

Now in Module 18:
We integrate SQLite directly into our Flask application!
Instead of storing tasks in a temporary Python list, our Flask routes will
now read and write directly to an SQLite database file.

What you will learn in this module:
1. Managing database connections per request using Flask's 'g' object
2. Automatically closing connections with @app.teardown_appcontext
3. GET /tasks -> Fetching rows from SQLite and returning JSON
4. POST /tasks -> Inserting a new task into SQLite from request data

Next Module Connection:
In Day 5 (Module 19), our application becomes larger. We will learn
Flask Blueprints to organize routes into clean, modular files!
=============================================================================
"""

import os
import sqlite3
from flask import Flask, g, jsonify, request

app = Flask(__name__)
DB_FILE = os.path.join(os.path.dirname(__file__), "module_18_tasks.db")

# =============================================================================
# 1. DATABASE HELPERS (Connection & Teardown)
# =============================================================================
def get_db():
    """Opens a connection for the current request if not already opened."""
    if "db" not in g:
        g.db = sqlite3.connect(DB_FILE)
        g.db.row_factory = sqlite3.Row  # Allows accessing columns by name: row['title']
    return g.db

@app.teardown_appcontext
def close_db(exception=None):
    """Closes the database connection when the request finishes."""
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    """Initializes the database table."""
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            status TEXT DEFAULT 'Pending'
        );
    """)
    conn.commit()
    conn.close()


# =============================================================================
# 2. FLASK ROUTES USING SQLITE
# =============================================================================

# GET /tasks: Read all tasks from SQLite
@app.route("/tasks", methods=["GET"])
def list_tasks():
    db = get_db()
    cursor = db.execute("SELECT id, title, status FROM tasks ORDER BY id ASC;")
    rows = cursor.fetchall()
    
    # Convert rows to standard Python dictionaries
    tasks = [dict(row) for row in rows]
    return jsonify({"success": True, "count": len(tasks), "tasks": tasks})


# POST /tasks: Insert a task into SQLite
@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json() or {}
    title = data.get("title", "").strip()
    status = data.get("status", "Pending")

    if not title:
        return jsonify({"success": False, "error": "Title is required"}), 400

    db = get_db()
    cursor = db.execute("INSERT INTO tasks (title, status) VALUES (?, ?);", (title, status))
    db.commit()

    return jsonify({
        "success": True,
        "message": "Task saved to database!",
        "task": {"id": cursor.lastrowid, "title": title, "status": status}
    }), 201


# =============================================================================
# RUNNING AND TESTING OUR CODE
# =============================================================================
if __name__ == "__main__":
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    init_db()
    client = app.test_client()

    print("--- STEP 1: POST /tasks (Adding Tasks to SQLite) ---")
    r1 = client.post("/tasks", json={"title": "Master Flask & SQLite", "status": "In Progress"})
    print("Created:", r1.get_json())

    r2 = client.post("/tasks", json={"title": "Learn Flask Blueprints", "status": "Pending"})
    print("Created:", r2.get_json())

    print("\n--- STEP 2: GET /tasks (Reading Tasks from SQLite) ---")
    r_get = client.get("/tasks")
    print("Database tasks retrieved:")
    print(r_get.get_json())

    # Clean up test DB file
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    print("\n[NEXT STEP] In Day 5 (Module 19), we will organize our routes using Blueprints!")
