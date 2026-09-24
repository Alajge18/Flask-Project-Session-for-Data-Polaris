"""
=============================================================================
MODULE 19: Project Architecture (Flask Blueprints)
Project Story: Building our "Task Manager" Architecture (Step 9)
=============================================================================
Welcome to Day 5!
Previously in Module 18:
We had all our task routes and database logic in one single file.

Now in Module 19:
As real backend apps grow, putting all routes in app.py creates "Spaghetti Code".
Flask solves this using BLUEPRINTS.
A Blueprint is a mini-app module that holds related routes:
- tasks_bp: Handles all task routes (/tasks)
- users_bp: Handles all user routes (/users)

What you will learn in this module:
1. Creating a Blueprint: tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')
2. Defining routes on the Blueprint
3. Registering the Blueprint on the main Flask app (app.register_blueprint)

Next Module Connection:
In Module 20, we will learn professional REST API Endpoint Design conventions!
=============================================================================
"""

from flask import Flask, Blueprint, jsonify

# =============================================================================
# 1. DEFINING THE TASKS BLUEPRINT
# =============================================================================
# url_prefix="/tasks" automatically prepends "/tasks" to all routes in this blueprint!
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

sample_tasks = [
    {"id": 1, "title": "Setup Blueprints", "status": "Completed"},
    {"id": 2, "title": "Organize Project Folders", "status": "In Progress"}
]

@tasks_bp.route("/", methods=["GET"])
def list_tasks():
    """Matches URL: /tasks/"""
    return jsonify({
        "blueprint": "tasks",
        "tasks": sample_tasks
    })

@tasks_bp.route("/<int:task_id>", methods=["GET"])
def get_task(task_id):
    """Matches URL: /tasks/<task_id>"""
    for t in sample_tasks:
        if t["id"] == task_id:
            return jsonify({"task": t})
    return jsonify({"error": "Task not found"}), 404


# =============================================================================
# 2. THE MAIN FLASK APPLICATION (Registering Blueprints)
# =============================================================================
app = Flask(__name__)

# Register our blueprint onto the main app
app.register_blueprint(tasks_bp)

@app.route("/")
def index():
    return jsonify({
        "message": "Welcome to Modular Task Manager!",
        "endpoints": ["/tasks/", "/tasks/<id>"]
    })


# =============================================================================
# RUNNING AND TESTING OUR CODE
# =============================================================================
if __name__ == "__main__":
    client = app.test_client()

    print("--- STEP 1: Testing Main App Route (GET /) ---")
    r1 = client.get("/")
    print(r1.get_json())

    print("\n--- STEP 2: Testing Blueprint Route (GET /tasks/) ---")
    r2 = client.get("/tasks/")
    print(r2.get_json())

    print("\n--- STEP 3: Testing Dynamic Blueprint Route (GET /tasks/1) ---")
    r3 = client.get("/tasks/1")
    print(r3.get_json())

    print("\n[NEXT STEP] In Module 20, we will learn REST API Endpoint Design!")
