# ============================================================
# models.py — Data Conversion Helpers (Module 4, 18)
# ============================================================
# This file converts database rows into Python dictionaries.
#
# Why do we need this?
#   When our API routes return JSON, Python needs dictionaries.
#   Database rows (sqlite3.Row objects) can't be directly
#   converted to JSON. So we convert them first:
#
#   Database Row → Dictionary → JSON
#
# Module 4  — Dictionaries and JSON Thinking
# Module 18 — Data conversion for Flask + SQLite
# ============================================================


def task_to_dict(task):
    """
    Convert a database task row to a Python dictionary.

    Module 4 — Dictionaries:
      Input:  sqlite3.Row object (from database query)
      Output: {"id": 1, "title": "...", "status": "...", ...}

      This dictionary is what jsonify() converts to JSON
      for our API responses.
    """
    return {
        "id": task["id"],
        "user_id": task["user_id"],
        "title": task["title"],
        "description": task["description"],
        "status": task["status"],
        "created_at": task["created_at"]
    }


def user_to_dict(user):
    """
    Convert a database user row to a Python dictionary.

    Module 4 — Dictionaries:
      Input:  sqlite3.Row object
      Output: {"id": 1, "name": "Alice", "email": "alice@email.com"}
    """
    return {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "created_at": user["created_at"]
    }


# --- Valid Task Statuses ---
# A task can only be one of these three statuses.
# We define this here so that app.py, forms.py, and database.py
# can all use the same list — no chance of typos or mismatches.
#
# Module 3 — Encapsulation: single source of truth for valid statuses
VALID_STATUSES = ["pending", "in_progress", "completed"]
# pending     → Task has not been started yet
# in_progress → Task is currently being worked on
# completed   → Task is finished
