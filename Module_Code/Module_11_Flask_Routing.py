"""
=============================================================================
MODULE 11: Flask Routing
PROJECT IMPLEMENTATION STARTS HERE!
Project: Task Manager Application (TaskFlow) — Step 1: Core Routing
=============================================================================
WELCOME TO THE PROJECT IMPLEMENTATION PHASE!
From this module forward (Module 11 to Module 26), we will build our real-world
hands-on backend application: The Task Manager System.

In Step 1 of our project, we implement core routing:
1. Static Route: GET /tasks (Show all tasks in our system)
2. Dynamic Route: GET /tasks/<int:task_id> (Show details of a specific task)
3. Type Safety: Flask's <int:task_id> converter rejects non-integer IDs (404)

Next Step in Project (Module 12):
We will add Task Filtering with query parameters (e.g. /tasks/filter?status=Pending)
and allow users to submit tasks!
=============================================================================
"""

from flask import Flask

app = Flask(__name__)

# Initial in-memory project data: Task Manager records
tasks = [
    {"id": 1, "title": "Setup Git Repository", "status": "Completed"},
    {"id": 2, "title": "Design Database Schema", "status": "In Progress"},
    {"id": 3, "title": "Build REST API Endpoints", "status": "Pending"}
]

# =============================================================================
# 1. STATIC ROUTE: List all tasks in Task Manager
# =============================================================================
@app.route("/tasks")
def list_tasks():
    """Returns a simple list of all tasks."""
    html_output = "<h2>TaskFlow — All Tasks</h2><ul>"
    for t in tasks:
        html_output += f"<li><a href='/tasks/{t['id']}'>Task #{t['id']}: {t['title']}</a> [{t['status']}]</li>"
    html_output += "</ul>"
    return html_output


# =============================================================================
# 2. DYNAMIC ROUTE: View a single task by ID
# =============================================================================
@app.route("/tasks/<int:task_id>")
def view_task_detail(task_id):
    """
    <int:task_id> is a dynamic converter.
    Matches /tasks/1, /tasks/2, etc.
    """
    for t in tasks:
        if t["id"] == task_id:
            return f"""
            <h3>Task Details (ID: {t['id']})</h3>
            <p><strong>Title:</strong> {t['title']}</p>
            <p><strong>Status:</strong> {t['status']}</p>
            <p><a href='/tasks'>&larr; Back to all tasks</a></p>
            """

    return f"<h3>Error: Task #{task_id} not found.</h3><p><a href='/tasks'>Back</a></p>", 404


# =============================================================================
# RUNNING AND TESTING OUR CODE
# =============================================================================
if __name__ == "__main__":
    client = app.test_client()

    print("--- 1. Testing GET /tasks (Project All Tasks List) ---")
    r1 = client.get("/tasks")
    print("Status:", r1.status_code)

    print("\n--- 2. Testing GET /tasks/1 (Single Task View) ---")
    r2 = client.get("/tasks/1")
    print(r2.data.decode("utf-8").strip())

    print("\n--- 3. Testing GET /tasks/999 (Not Found) ---")
    r3 = client.get("/tasks/999")
    print("Status:", r3.status_code)

    print("\n[PROJECT STEP 1 COMPLETE]")
    print("Next in Module 12: Adding task search and query filtering!")
