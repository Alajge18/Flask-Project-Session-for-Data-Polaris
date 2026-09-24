"""
=============================================================================
MODULE 12: Query Parameters and Request Data
Project Story: Building our "Task Manager" Web App (Step 2)
=============================================================================
Previously in Module 11 (Step 1):
We built dynamic routes like /tasks/<int:task_id>.

Now in Module 12:
Users want to filter tasks (e.g. "show only pending tasks") and send data to
the server. Flask gives us the 'request' object to read client data:

1. request.args: Reads URL Query Parameters (e.g. /tasks/filter?status=Pending)
2. request.form: Reads HTML Form submissions (from <form method="POST">)
3. request.get_json(): Reads JSON payloads from API clients

What you will learn in this module:
- Reading query strings with request.args.get()
- Reading form data with request.form.get()
- Reading JSON with request.get_json()

Next Module Connection:
In Module 13, we will use Jinja2 templates so we don't have to write HTML
strings inside Python functions!
=============================================================================
"""

from flask import Flask, request, jsonify

app = Flask(__name__)

tasks = [
    {"id": 1, "title": "Buy Milk", "status": "Completed"},
    {"id": 2, "title": "Finish Flask Project", "status": "Pending"},
    {"id": 3, "title": "Review Python Concepts", "status": "Pending"}
]

# =============================================================================
# 1. QUERY PARAMETERS: request.args (URL: /tasks/filter?status=Pending)
# =============================================================================
@app.route("/tasks/filter", methods=["GET"])
def filter_tasks():
    # Read the ?status=... value from the URL (defaults to None if missing)
    status = request.args.get("status")

    if status:
        filtered = [t for t in tasks if t["status"].lower() == status.lower()]
    else:
        filtered = tasks

    return jsonify({
        "filter_applied": status,
        "count": len(filtered),
        "tasks": filtered
    })


# =============================================================================
# 2. FORM DATA: request.form (Submitted from an HTML Form)
# =============================================================================
@app.route("/tasks/add-form", methods=["POST"])
def add_task_from_form():
    # Read data submitted via standard HTML <form>
    title = request.form.get("title")
    
    if not title:
        return "Error: Task title is required!", 400

    new_task = {"id": len(tasks) + 1, "title": title, "status": "Pending"}
    tasks.append(new_task)
    return f"Success! Created task: {new_task['title']}", 201


# =============================================================================
# 3. JSON DATA: request.get_json() (Submitted by Frontend/Postman)
# =============================================================================
@app.route("/tasks/add-json", methods=["POST"])
def add_task_from_json():
    # Read JSON sent in HTTP request body
    data = request.get_json()
    title = data.get("title")

    new_task = {"id": len(tasks) + 1, "title": title, "status": data.get("status", "Pending")}
    tasks.append(new_task)
    return jsonify({"message": "Task added via JSON", "task": new_task}), 201


# =============================================================================
# RUNNING AND TESTING OUR CODE
# =============================================================================
if __name__ == "__main__":
    client = app.test_client()

    print("--- STEP 1: Query String Filtering (?status=Pending) ---")
    r1 = client.get("/tasks/filter?status=Pending")
    print(r1.get_json())

    print("\n--- STEP 2: Submitting an HTML Form (request.form) ---")
    r2 = client.post("/tasks/add-form", data={"title": "Submit Assignment"})
    print("Status:", r2.status_code, "->", r2.data.decode("utf-8"))

    print("\n--- STEP 3: Submitting JSON Payload (request.get_json) ---")
    r3 = client.post("/tasks/add-json", json={"title": "Learn Jinja2 Templates", "status": "In Progress"})
    print("Status:", r3.status_code, "->", r3.get_json())

    print("\n[NEXT STEP] In Module 13, we will render beautiful HTML pages using Jinja2 templates!")
