"""
=============================================================================
MODULE 20: REST API Endpoint Design
Project Story: Building our "Task Manager" API (Step 10)
=============================================================================
Previously in Module 19:
We organized routes using Blueprints.

Now in Module 20:
How do top backend engineers design clean, professional REST URLs?

The 3 Golden Rules:
1. Use NOUNS, not verbs:
   [BAD]  : /api/getTasks, /api/createTask, /api/deleteTask
   [GOOD] : GET /api/tasks, POST /api/tasks, DELETE /api/tasks/1

2. Use PLURAL names for collections:
   [GOOD] : /api/tasks, /api/users

3. Return consistent JSON envelopes:
   {"success": true, "data": ...}

What you will learn in this module:
- Structuring clean REST URLs
- Creating standard helper functions for consistent JSON responses
- Sub-resource design (e.g. /api/users/1/tasks)

Next Module Connection:
In Module 21, we will add Validation and Error Handling to protect our API!
=============================================================================
"""

from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data
tasks = [
    {"id": 1, "user_id": 101, "title": "Setup REST API", "status": "Completed"},
    {"id": 2, "user_id": 101, "title": "Design Clean Endpoints", "status": "In Progress"},
    {"id": 3, "user_id": 102, "title": "Write Unit Tests", "status": "Pending"}
]

# =============================================================================
# 1. CONSISTENT JSON RESPONSE HELPER
# =============================================================================
def api_response(success, data=None, message="", status_code=200):
    """Helper to return consistent JSON across all endpoints."""
    return jsonify({
        "success": success,
        "message": message,
        "data": data
    }), status_code


# =============================================================================
# 2. CLEAN RESTFUL ENDPOINTS
# =============================================================================

# GET /api/tasks (Collection)
@app.route("/api/tasks", methods=["GET"])
def get_all_tasks():
    return api_response(success=True, data=tasks, message="Tasks fetched successfully")


# GET /api/tasks/<id> (Individual Resource)
@app.route("/api/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    for t in tasks:
        if t["id"] == task_id:
            return api_response(success=True, data=t)
    return api_response(success=False, message="Task not found", status_code=404)


# GET /api/users/<user_id>/tasks (Nested Sub-Resource)
@app.route("/api/users/<int:user_id>/tasks", methods=["GET"])
def get_user_tasks(user_id):
    """Fetches only the tasks assigned to a specific user."""
    user_tasks = [t for t in tasks if t["user_id"] == user_id]
    return api_response(success=True, data=user_tasks, message=f"Tasks for user {user_id}")


# =============================================================================
# RUNNING AND TESTING OUR CODE
# =============================================================================
if __name__ == "__main__":
    client = app.test_client()

    print("--- STEP 1: GET /api/tasks (All Tasks) ---")
    r1 = client.get("/api/tasks")
    print(r1.get_json())

    print("\n--- STEP 2: GET /api/tasks/1 (Single Task) ---")
    r2 = client.get("/api/tasks/1")
    print(r2.get_json())

    print("\n--- STEP 3: GET /api/users/101/tasks (User Sub-Resource) ---")
    r3 = client.get("/api/users/101/tasks")
    print(r3.get_json())

    print("\n[NEXT STEP] In Module 21, we will add error handling and validation!")
