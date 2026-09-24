# ============================================================
# routes/task_routes.py — Task Route Blueprint (Module 19, 20, 21)
# ============================================================
# All task-related routes are here — both HTML pages and JSON APIs.
#
# Module 19 — Project Architecture: Blueprint for task routes
# Module 20 — API Endpoint Design: REST endpoints
# Module 21 — Validation & Error Handling
# Module 11 — Flask Routing: static & dynamic routes
# Module 12 — Query Parameters: request.args
# Module 13 — HTML Forms + Jinja2: render_template, flash, redirect
# Module 14 — Flask-WTF: form validation
# Module 15 — APIs and JSON: jsonify, request.get_json()
# ============================================================

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
# Blueprint → Creates a mini-app that we register with the main app
# This lets us organize routes into separate files (Module 19)

from database import (
    get_all_tasks, get_task_by_id, get_tasks_by_status,
    get_task_counts, create_task, update_task, delete_task, search_tasks
)
# Import database functions — this file doesn't write SQL directly
# Module 19 — Separation of Concerns

from models import task_to_dict, VALID_STATUSES
# Module 4 — Dictionary conversion for JSON responses

from forms import AddTaskForm, EditTaskForm
# Module 14 — Flask-WTF form classes


# --- Create the Blueprint ---
# Module 19 — Blueprints:
#   "tasks" → Blueprint name (used internally by Flask)
#   __name__ → Tells Flask where this file is located
task_bp = Blueprint("tasks", __name__)


# ============================================================
# HTML ROUTES — These return web pages (Module 13 — Jinja2)
# ============================================================

# --- Homepage / Dashboard ---
# Module 10 — First Flask Route
# Module 11 — Static Route
@task_bp.route("/")
def home():
    """Show the homepage with task stats."""
    counts = get_task_counts()
    return render_template("index.html", counts=counts)
    # Module 13 — render_template passes 'counts' dict to the template
    # In index.html: {{ counts.total }}, {{ counts.pending }}, etc.


# --- About Page ---
# Module 10 — Basic Flask Routes
@task_bp.route("/about")
def about():
    """Show the about page."""
    return render_template("about.html")


# --- List All Tasks (with optional status filter) ---
# Module 11 — Static Route
# Module 12 — Query Parameters: request.args.get("status")
@task_bp.route("/tasks")
def list_tasks():
    """
    Show all tasks. Supports filtering by status using query parameters.

    Module 12 — Query Parameters:
      /tasks              → shows ALL tasks
      /tasks?status=pending → shows only pending tasks
    """
    status = request.args.get("status")
    # Module 12: request.args.get() reads query parameters from the URL

    if status and status in VALID_STATUSES:
        all_tasks = get_tasks_by_status(status)
    else:
        all_tasks = get_all_tasks()

    return render_template("tasks.html", tasks=all_tasks, current_status=status, search_query="")


# --- Search Tasks ---
# Module 12 — Query Parameters
@task_bp.route("/tasks/search")
def search():
    """
    Search tasks by title or description.

    Module 12 — Query Parameters:
      /tasks/search?q=flask          → tasks matching 'flask'
      /tasks/search?q=flask&status=pending → only pending matching 'flask'
    """
    query = request.args.get("q", "").strip()
    status = request.args.get("status", "").strip()

    if not query:
        return redirect(url_for("tasks.list_tasks"))
        # Module 13 — Redirects: url_for uses "blueprint_name.function_name"

    if status and status in VALID_STATUSES:
        results = search_tasks(query, status=status)
    else:
        results = search_tasks(query)
        status = None

    return render_template(
        "tasks.html",
        tasks=results,
        current_status=status,
        search_query=query
    )


# --- View One Task ---
# Module 11 — Dynamic Route with int converter
@task_bp.route("/tasks/<int:task_id>")
def task_detail(task_id):
    """
    Show details of a single task.

    Module 11 — Dynamic Routes:
      <int:task_id> means Flask grabs the number from the URL
      /tasks/3 → task_id=3 (automatically converted to integer)
    """
    task = get_task_by_id(task_id)

    if not task:
        # Module 6, 21 — Error Handling: task doesn't exist
        flash("Task not found.", "error")
        # Module 13 — Flash Messages: one-time notification
        return redirect(url_for("tasks.list_tasks"))

    return render_template("task_detail.html", task=task)


# --- Add a New Task (Form Page) ---
# Module 13 — HTML Forms: GET shows form, POST processes it
# Module 14 — Flask-WTF: form validation
@task_bp.route("/tasks/add", methods=["GET", "POST"])
def add_task():
    """
    Show the add task form (GET) or save a new task (POST).

    Module 14 — Flask-WTF Workflow:
      1. GET request → show empty form
      2. User fills in fields and clicks Submit
      3. POST request → validate with form.validate_on_submit()
      4. If valid → save to database, redirect with flash
      5. If invalid → re-show form with error messages
    """
    form = AddTaskForm()
    # Module 3 — OOP: Create form object from AddTaskForm class

    if form.validate_on_submit():
        # Module 14: validate_on_submit() checks:
        #   1. Is it a POST request?
        #   2. Do all validators pass?
        # If BOTH are True → we can safely save the data

        create_task(
            form.title.data,        # Task title from the form
            form.description.data,  # Task description from the form
            "pending"               # New tasks always start as "pending"
        )
        flash("Task created successfully!", "success")
        # Module 13 — Flash Messages
        return redirect(url_for("tasks.list_tasks"))
        # Module 13 — Post/Redirect/Get pattern

    return render_template("add_task.html", form=form)


# --- Edit a Task (Form Page) ---
# Module 11 — Dynamic Route
# Module 14 — Flask-WTF: pre-filled form
@task_bp.route("/tasks/<int:task_id>/edit", methods=["GET", "POST"])
def edit_task(task_id):
    """
    Show the edit form pre-filled with current data (GET) or save changes (POST).

    Module 14 — Flask-WTF:
      On GET: Pre-fill form fields with current task data
      On POST: Validate and save updated data
    """
    task = get_task_by_id(task_id)

    if not task:
        flash("Task not found.", "error")
        return redirect(url_for("tasks.list_tasks"))

    form = EditTaskForm()

    if form.validate_on_submit():
        update_task(task_id, form.title.data, form.description.data, form.status.data)
        flash("Task updated successfully!", "success")
        return redirect(url_for("tasks.task_detail", task_id=task_id))

    # Module 14: Pre-fill form with existing data on GET request
    if request.method == "GET":
        form.title.data = task["title"]
        form.description.data = task["description"]
        form.status.data = task["status"]

    return render_template("edit_task.html", form=form, task=task)


# --- Delete a Task ---
# Module 11 — Dynamic Route
@task_bp.route("/tasks/<int:task_id>/delete")
def delete_task_route(task_id):
    """Delete a task and redirect to the task list."""
    task = get_task_by_id(task_id)

    if not task:
        flash("Task not found.", "error")
    else:
        delete_task(task_id)
        flash("Task deleted.", "success")

    return redirect(url_for("tasks.list_tasks"))


# ============================================================
# JSON API ROUTES — These return JSON data (Module 15)
# ============================================================
# APIs are used by other programs (mobile apps, Postman, curl)
# instead of web browsers. They send and receive JSON.
#
# Key differences from HTML routes:
#   - Return jsonify({...}) instead of render_template(...)
#   - Read JSON with request.get_json() instead of form data
#   - Use HTTP methods: GET, POST, PUT, DELETE
#   - Return status codes: 200, 201, 400, 404
#
# Module 15 — APIs and JSON
# Module 8  — HTTP Methods
# Module 9  — HTTP Status Codes
# Module 20 — API Endpoint Design
# Module 21 — Validation & Error Handling
# ============================================================


# --- API: Create a Task ---
# Module 8 — HTTP Methods: POST = Create
# Module 9 — Status Codes: 201 Created, 400 Bad Request
@task_bp.route("/api/tasks", methods=["POST"])
def api_create_task():
    """
    Create a new task via JSON.

    Module 15 — APIs:
      Expected JSON body:
        {"title": "Learn Flask", "description": "...", "user_id": 1}

    Module 21 — Validation:
      - Title is required
      - Status must be valid (if provided)
    """
    data = request.get_json()
    # Module 15: request.get_json() reads JSON from the request body

    # Module 21 — Validation: Check required fields
    if not data or not data.get("title"):
        return jsonify({"error": "Title is required."}), 400
        # Module 9: 400 Bad Request

    # Module 21 — Validation: Check status value
    if data.get("status") and data["status"] not in VALID_STATUSES:
        return jsonify({"error": f"Invalid status. Use: {VALID_STATUSES}"}), 400

    status = data.get("status", "pending")
    # Module 1 — Default Arguments: default to "pending"
    user_id = data.get("user_id")

    task_id = create_task(data["title"], data.get("description", ""), status, user_id)
    task = get_task_by_id(task_id)

    return jsonify({
        "message": "Task created successfully",
        "task": task_to_dict(task)
        # Module 4: Convert database row to dictionary for JSON
    }), 201
    # Module 9: 201 Created


# --- API: List All Tasks ---
# Module 8 — HTTP Methods: GET = Read
# Module 12 — Query Parameters: ?status= filter
@task_bp.route("/api/tasks", methods=["GET"])
def api_get_tasks():
    """
    Return all tasks as JSON. Supports ?status= filter.

    Module 12 — Query Parameters:
      GET /api/tasks              → all tasks
      GET /api/tasks?status=pending → only pending tasks
    """
    status = request.args.get("status")

    if status:
        if status not in VALID_STATUSES:
            return jsonify({"error": f"Invalid status. Use: {VALID_STATUSES}"}), 400
        tasks = get_tasks_by_status(status)
    else:
        tasks = get_all_tasks()

    return jsonify([task_to_dict(t) for t in tasks]), 200
    # Module 4: List comprehension → list of dictionaries → JSON array


# --- API: Get One Task ---
# Module 11 — Dynamic Route: <int:task_id>
@task_bp.route("/api/tasks/<int:task_id>", methods=["GET"])
def api_get_task(task_id):
    """Return one task by ID as JSON."""
    task = get_task_by_id(task_id)

    if not task:
        return jsonify({"error": "Task not found."}), 404
        # Module 9: 404 Not Found

    return jsonify(task_to_dict(task)), 200


# --- API: Update a Task ---
# Module 8 — HTTP Methods: PUT = Update
@task_bp.route("/api/tasks/<int:task_id>", methods=["PUT"])
def api_update_task(task_id):
    """
    Update an existing task via JSON.

    PUT means "replace/update this resource".
    Only the fields you send will be updated.
    Fields you don't send keep their current values.
    """
    task = get_task_by_id(task_id)
    if not task:
        return jsonify({"error": "Task not found."}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required."}), 400

    # Module 1 — Default Arguments:
    # Use new values if provided, otherwise keep old values
    title = data.get("title", task["title"])
    description = data.get("description", task["description"])
    status = data.get("status", task["status"])

    # Module 21 — Validation
    if status not in VALID_STATUSES:
        return jsonify({"error": f"Invalid status. Use: {VALID_STATUSES}"}), 400

    update_task(task_id, title, description, status)
    updated = get_task_by_id(task_id)

    return jsonify({
        "message": "Task updated successfully",
        "task": task_to_dict(updated)
    }), 200


# --- API: Delete a Task ---
# Module 8 — HTTP Methods: DELETE = Delete
@task_bp.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def api_delete_task(task_id):
    """Delete a task by ID."""
    task = get_task_by_id(task_id)

    if not task:
        return jsonify({"error": "Task not found."}), 404

    delete_task(task_id)

    return jsonify({"message": "Task deleted successfully"}), 200
