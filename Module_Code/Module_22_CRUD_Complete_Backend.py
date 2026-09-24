"""
=============================================================================
MODULE 22: Complete CRUD Backend Integration
Project Story: The Complete Task Manager Backend (Step 12 — Capstone Integration)
=============================================================================
CONGRATULATIONS! You have reached the Capstone Module of Day 5.

This single file brings together everything learned across Days 1 to 5:
- Day 1: Functions, Scope, and Data Structures
- Day 2-3: Flask, Routing, and REST APIs
- Day 4: SQLite Database Persistence
- Day 5: Validation, Clean Endpoints, and Error Handling

Complete CRUD API Endpoints:
  1. POST   /api/tasks      -> Create a new task in SQLite (Create)
  2. GET    /api/tasks      -> Read all tasks from SQLite (Read All)
  3. GET    /api/tasks/<id> -> Read a specific task (Read One)
  4. PUT    /api/tasks/<id> -> Update task title and status (Update)
  5. DELETE /api/tasks/<id> -> Delete task from SQLite (Delete)

Next Module Connection:
In Day 6 (Modules 23 to 26), we will prepare this application for PRODUCTION
and deploy it live to the internet (Render & Vercel)!
=============================================================================
"""

import os
import sqlite3
from flask import Flask, jsonify, request, g

app = Flask(__name__)
DB_FILE = os.path.join(os.path.dirname(__file__), "tasks_master.db")

# =============================================================================
# 1. DATABASE HELPERS
# =============================================================================
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_FILE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
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
# 2. REST API CRUD ENDPOINTS
# =============================================================================

# 1. CREATE: POST /api/tasks
@app.route("/api/tasks", methods=["POST"])
def create_task():
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
        "message": "Task created successfully",
        "task": {"id": cursor.lastrowid, "title": title, "status": status}
    }), 201


# 2. READ ALL: GET /api/tasks
@app.route("/api/tasks", methods=["GET"])
def get_all_tasks():
    db = get_db()
    cursor = db.execute("SELECT id, title, status FROM tasks ORDER BY id ASC;")
    tasks = [dict(row) for row in cursor.fetchall()]
    return jsonify({"success": True, "count": len(tasks), "tasks": tasks}), 200


# 3. READ ONE: GET /api/tasks/<id>
@app.route("/api/tasks/<int:task_id>", methods=["GET"])
def get_single_task(task_id):
    db = get_db()
    cursor = db.execute("SELECT id, title, status FROM tasks WHERE id = ?;", (task_id,))
    row = cursor.fetchone()

    if not row:
        return jsonify({"success": False, "error": f"Task #{task_id} not found"}), 404

    return jsonify({"success": True, "task": dict(row)}), 200


# 4. UPDATE: PUT /api/tasks/<id>
@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json() or {}
    title = data.get("title", "").strip()
    status = data.get("status", "Pending")

    if not title:
        return jsonify({"success": False, "error": "Title cannot be empty"}), 400

    db = get_db()
    cursor = db.execute("UPDATE tasks SET title = ?, status = ? WHERE id = ?;", (title, status, task_id))
    db.commit()

    if cursor.rowcount == 0:
        return jsonify({"success": False, "error": f"Task #{task_id} not found"}), 404

    return jsonify({
        "success": True,
        "message": "Task updated successfully",
        "task": {"id": task_id, "title": title, "status": status}
    }), 200


# 5. DELETE: DELETE /api/tasks/<id>
@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    db = get_db()
    cursor = db.execute("DELETE FROM tasks WHERE id = ?;", (task_id,))
    db.commit()

    if cursor.rowcount == 0:
        return jsonify({"success": False, "error": f"Task #{task_id} not found"}), 404

    return jsonify({"success": True, "message": f"Task #{task_id} deleted successfully"}), 200


# =============================================================================
# RUNNING AND TESTING THE COMPLETE CRUD SYSTEM
# =============================================================================
if __name__ == "__main__":
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    init_db()
    client = app.test_client()

    print("--- 1. [CREATE] Adding Tasks ---")
    c1 = client.post("/api/tasks", json={"title": "Build Flask Backend", "status": "In Progress"})
    print("Created:", c1.get_json())
    c2 = client.post("/api/tasks", json={"title": "Deploy to Cloud", "status": "Pending"})
    print("Created:", c2.get_json())

    print("\n--- 2. [READ ALL] Fetching All Tasks ---")
    print(client.get("/api/tasks").get_json())

    print("\n--- 3. [READ ONE] Fetching Task #1 ---")
    print(client.get("/api/tasks/1").get_json())

    print("\n--- 4. [UPDATE] Updating Task #1 to Completed ---")
    u1 = client.put("/api/tasks/1", json={"title": "Build Flask Backend", "status": "Completed"})
    print(u1.get_json())

    print("\n--- 5. [DELETE] Deleting Task #2 ---")
    d1 = client.delete("/api/tasks/2")
    print(d1.get_json())

    print("\n--- 6. [VERIFY] Final Database State ---")
    print(client.get("/api/tasks").get_json())

    # Clean up test DB file
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    print("\n[NEXT STEP] In Day 6, we deploy this backend to Render and Vercel!")
