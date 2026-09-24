"""
=============================================================================
MODULE 15: Building RESTful APIs with JSON
Project Story: Building our "Task Manager" API (Step 5)
=============================================================================
Previously in Module 14:
We rendered HTML web pages with forms.

Now in Module 15:
Instead of HTML web pages, modern backends often operate as REST APIs.
A REST API returns pure JSON data that mobile apps, React, Vue, or Postman
can easily consume.

What you will learn in this module:
1. Using Flask's jsonify() function
2. GET /api/tasks -> Returning all tasks as JSON
3. POST /api/tasks -> Creating a new task from JSON payload
4. DELETE /api/tasks/<id> -> Deleting a task

Next Module Connection:
Notice that our tasks are stored in a Python list. If we stop the server,
ALL DATA IS LOST!
In Module 16 (Day 4), we begin DATABASES so tasks are saved permanently!
=============================================================================
"""

from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory task list
tasks = [
    {"id": 1, "title": "Learn Flask Basics", "status": "Completed"},
    {"id": 2, "title": "Build a REST API", "status": "In Progress"}
]

# =============================================================================
# 1. GET /api/tasks (Retrieve all tasks as JSON)
# =============================================================================
@app.route("/api/tasks", methods=["GET"])
def get_all_tasks():
    # jsonify converts our Python list into a JSON response with Content-Type: application/json
    return jsonify({
        "success": True,
        "count": len(tasks),
        "tasks": tasks
    }), 200


# =============================================================================
# 2. POST /api/tasks (Create a new task from JSON)
# =============================================================================
@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json()

    if not data or "title" not in data or not data["title"]:
        return jsonify({"success": False, "error": "Task title is required!"}), 400

    new_task = {
        "id": len(tasks) + 1,
        "title": data["title"],
        "status": data.get("status", "Pending")
    }
    tasks.append(new_task)

    return jsonify({
        "success": True,
        "message": "Task created successfully!",
        "task": new_task
    }), 201


# =============================================================================
# 3. DELETE /api/tasks/<id> (Remove a task)
# =============================================================================
@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    for idx, t in enumerate(tasks):
        if t["id"] == task_id:
            removed = tasks.pop(idx)
            return jsonify({"success": True, "message": f"Deleted '{removed['title']}'"}), 200

    return jsonify({"success": False, "error": "Task not found"}), 404


# =============================================================================
# RUNNING AND TESTING OUR CODE
# =============================================================================
if __name__ == "__main__":
    client = app.test_client()

    print("--- STEP 1: GET /api/tasks (Fetch JSON List) ---")
    r1 = client.get("/api/tasks")
    print("Status:", r1.status_code)
    print("Response JSON:", r1.get_json())

    print("\n--- STEP 2: POST /api/tasks (Create New Task via JSON) ---")
    r2 = client.post("/api/tasks", json={"title": "Connect SQLite Database", "status": "Pending"})
    print("Status:", r2.status_code)
    print("Response JSON:", r2.get_json())

    print("\n--- STEP 3: DELETE /api/tasks/1 (Delete Task) ---")
    r3 = client.delete("/api/tasks/1")
    print("Status:", r3.status_code)
    print("Response JSON:", r3.get_json())

    print("\n[NEXT STEP] In Day 4 (Module 16), we learn Databases so data persists permanently!")
