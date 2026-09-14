# ============================================================
# models.py — Data Conversion Helpers
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
# This file also defines the list of valid task statuses,
# so all parts of the app use the same list.
# ============================================================


def user_to_dict(user):
    """
    Convert a database user row to a Python dictionary.
    
    Input:  sqlite3.Row object (from database query)
    Output: {"id": 1, "name": "Alice", "email": "alice@example.com"}
    
    This dictionary can then be converted to JSON by jsonify()
    """
    return {
        "id": user["id"],         # user["id"] works because of row_factory = sqlite3.Row
        "name": user["name"],     # Access column values by name
        "email": user["email"]
    }


def task_to_dict(task):
    """
    Convert a database task row to a Python dictionary.
    
    Input:  sqlite3.Row object (from database query)
    Output: {"id": 1, "title": "...", "description": "...", "status": "...", "user_id": 1}
    """
    return {
        "id": task["id"],
        "title": task["title"],
        "description": task["description"],
        "status": task["status"],
        "user_id": task["user_id"]
    }


# --- Valid Task Statuses ---
# A task can only be one of these three statuses.
# We define this here so that app.py, forms.py, and database.py
# can all use the same list — no chance of typos or mismatches.
VALID_STATUSES = ["pending", "in_progress", "completed"]
# pending     → Task has not been started yet
# in_progress → Task is currently being worked on
# completed   → Task is finished
