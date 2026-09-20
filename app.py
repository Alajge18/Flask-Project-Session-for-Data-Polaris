# ============================================================
# app.py — The Main Entry Point of TaskFlow
# ============================================================
# Personal Task Management System
# No admin panel, no user management — just YOUR tasks.
# View, Add, Edit, Delete your tasks easily.
# ============================================================

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
# Flask         → The framework itself, creates our web app
# render_template → Turns HTML template files into web pages
# request       → Gives us access to data sent by the browser (form data, JSON, URL params)
# redirect      → Sends the browser to a different URL
# url_for       → Generates a URL from a function name (safer than hardcoding URLs)
# flash         → Shows a one-time message to the user (like "Task created!")
# jsonify       → Converts Python dictionaries to JSON responses for APIs

import os
import database

# Vercel's filesystem is read-only except for /tmp.
# Keep the normal local database when running locally, but use
# /tmp on Vercel so the SQLite database can be opened.
if os.environ.get("VERCEL"):
    database.DATABASE = "/tmp/tasks.db"

from database import init_db
from database import get_all_tasks, get_task_by_id, get_tasks_by_status, get_task_counts
from database import create_task, update_task, delete_task, search_tasks
# We import all our database functions from database.py
# This keeps app.py clean — it doesn't need to know SQL

from models import task_to_dict, VALID_STATUSES
# task_to_dict → Convert database rows to dictionaries (for JSON)
# VALID_STATUSES → List of allowed statuses: ["pending", "in_progress", "completed"]

from forms import AddTaskForm, EditTaskForm
# These are Flask-WTF form classes that handle form validation


# --- Create the Flask Application ---
app = Flask(__name__)
# Flask(__name__) creates a new web application
# __name__ tells Flask where this file is located, so it can find templates/ and static/

app.config["SECRET_KEY"] = "my-secret-key-for-learning"
# SECRET_KEY is required by Flask-WTF for CSRF protection
# CSRF protection prevents fake form submissions from other websites
# In a real app, use a long random string and keep it secret


# --- Initialize the Database ---
with app.app_context():
    init_db()
# This runs init_db() when the app starts
# init_db() creates the tasks table if it doesn't exist yet
# app_context() is needed because database operations require Flask to be "active"


# ============================================================
# HTML ROUTES — These return web pages that users see in the browser
# ============================================================
# Each route has:
#   @app.route("/some-url")  → What URL triggers this function
#   def function_name():     → The function that runs
#   return render_template() → Sends back an HTML page
# ============================================================


# --- Homepage / Dashboard ---
@app.route("/")
def home():
    """Show the homepage with task stats."""
    # Get task counts for the dashboard stats
    counts = get_task_counts()
    return render_template("index.html", counts=counts)


# --- List All Tasks (with optional status filter) ---
@app.route("/tasks")
def tasks():
    """
    Show all tasks. Supports filtering by status using query parameters.
    
    Examples:
      /tasks              → shows ALL tasks
      /tasks?status=pending → shows only pending tasks
    """
    status = request.args.get("status")

    if status and status in VALID_STATUSES:
        all_tasks = get_tasks_by_status(status)
    else:
        all_tasks = get_all_tasks()

    return render_template("tasks.html", tasks=all_tasks, current_status=status, search_query="")


# --- Search Tasks ---
@app.route("/tasks/search")
def search():
    """
    Search tasks by title or description.

    Examples:
      /tasks/search?q=flask          → tasks matching 'flask'
      /tasks/search?q=flask&status=pending → only pending tasks matching 'flask'
    """
    query = request.args.get("q", "").strip()
    status = request.args.get("status", "").strip()

    if not query:
        return redirect(url_for("tasks"))

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
@app.route("/tasks/<int:task_id>")
def task_detail(task_id):
    """
    Show details of a single task.
    
    <int:task_id> in the URL means:
      - Flask grabs the number from the URL (e.g., /tasks/3 → task_id=3)
      - Converts it to an integer automatically
      - Passes it to this function
    """
    task = get_task_by_id(task_id)  # Find the task in the database

    if not task:
        # Task doesn't exist → show error and go back to task list
        flash("Task not found.", "error")
        return redirect(url_for("tasks"))

    return render_template("task_detail.html", task=task)


# --- Add a New Task (Form Page) ---
@app.route("/tasks/add", methods=["GET", "POST"])
def add_task():
    """Show the add task form (GET) or save a new task (POST)."""
    form = AddTaskForm()

    if form.validate_on_submit():
        # All checks passed → save the task
        create_task(
            form.title.data,        # Task title from the form
            form.description.data,  # Task description from the form
            "pending"               # New tasks always start as "pending"
        )
        flash("Task created successfully!", "success")
        return redirect(url_for("tasks"))  # Go to task list

    return render_template("add_task.html", form=form)


# --- Edit a Task (Form Page) ---
@app.route("/tasks/<int:task_id>/edit", methods=["GET", "POST"])
def edit_task(task_id):
    """Show the edit form pre-filled with current data (GET) or save changes (POST)."""
    task = get_task_by_id(task_id)

    if not task:
        flash("Task not found.", "error")
        return redirect(url_for("tasks"))

    form = EditTaskForm()

    if form.validate_on_submit():
        # Save the updated data to the database
        update_task(task_id, form.title.data, form.description.data, form.status.data)
        flash("Task updated successfully!", "success")
        return redirect(url_for("task_detail", task_id=task_id))

    # When the page first loads (GET request), fill the form with existing data
    # So the user sees the current title, description, and status
    if request.method == "GET":
        form.title.data = task["title"]
        form.description.data = task["description"]
        form.status.data = task["status"]

    return render_template("edit_task.html", form=form, task=task)


# --- Delete a Task ---
@app.route("/tasks/<int:task_id>/delete")
def delete_task_route(task_id):
    """Delete a task and redirect to the task list."""
    # Note: Function name is delete_task_route (not delete_task)
    # because delete_task is already the name of our database function
    task = get_task_by_id(task_id)

    if not task:
        flash("Task not found.", "error")
    else:
        delete_task(task_id)  # Remove from database
        flash("Task deleted.", "success")

    return redirect(url_for("tasks"))  # Always go back to task list


# ============================================================
# JSON API ROUTES — These return JSON data (not web pages)
# ============================================================
# APIs are used by other programs (mobile apps, Postman, curl)
# instead of web browsers. They send and receive JSON.
#
# Key differences from HTML routes:
#   - Return jsonify({...}) instead of render_template(...)
#   - Read JSON with request.get_json() instead of form data
#   - Use HTTP methods: GET (read), POST (create), PUT (update), DELETE (remove)
#   - Return status codes: 200 (OK), 201 (Created), 400 (Bad Request), 404 (Not Found)
# ============================================================


# --- API: Create a Task ---
@app.route("/api/tasks", methods=["POST"])
def api_create_task():
    """
    Create a new task via JSON.
    
    Expected JSON body:
      {"title": "Learn Flask", "description": "...", "status": "pending"}
    """
    data = request.get_json()

    # Validate required fields
    if not data or not data.get("title"):
        return jsonify({"error": "Title is required."}), 400

    # Validate status (if provided)
    if data.get("status") and data["status"] not in VALID_STATUSES:
        return jsonify({"error": f"Invalid status. Use: {VALID_STATUSES}"}), 400

    # Set default status to "pending" if not provided
    status = data.get("status", "pending")

    # Save to database
    task_id = create_task(data["title"], data.get("description", ""), status)
    task = get_task_by_id(task_id)

    return jsonify({
        "message": "Task created successfully",
        "task": task_to_dict(task)
    }), 201


# --- API: List All Tasks (with optional filter) ---
@app.route("/api/tasks", methods=["GET"])
def api_get_tasks():
    """
    Return all tasks as JSON. Supports ?status= filter.
    
    Examples:
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


# --- API: Get One Task ---
@app.route("/api/tasks/<int:task_id>", methods=["GET"])
def api_get_task(task_id):
    """Return one task by ID as JSON."""
    task = get_task_by_id(task_id)

    if not task:
        return jsonify({"error": "Task not found."}), 404

    return jsonify(task_to_dict(task)), 200


# --- API: Update a Task ---
@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def api_update_task(task_id):
    """
    Update an existing task via JSON.
    
    PUT means "replace/update this resource".
    Only the fields you send will be updated.
    Fields you don't send will keep their current values.
    """
    task = get_task_by_id(task_id)
    if not task:
        return jsonify({"error": "Task not found."}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required."}), 400

    # Use new values if provided, otherwise keep the old values
    title = data.get("title", task["title"])
    description = data.get("description", task["description"])
    status = data.get("status", task["status"])

    # Validate the status
    if status not in VALID_STATUSES:
        return jsonify({"error": f"Invalid status. Use: {VALID_STATUSES}"}), 400

    update_task(task_id, title, description, status)  # Save changes
    updated = get_task_by_id(task_id)  # Fetch the updated task

    return jsonify({
        "message": "Task updated successfully",
        "task": task_to_dict(updated)
    }), 200


# --- API: Delete a Task ---
@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def api_delete_task(task_id):
    """
    Delete a task by ID.
    
    DELETE method tells the server to remove this resource.
    """
    task = get_task_by_id(task_id)

    if not task:
        return jsonify({"error": "Task not found."}), 404

    delete_task(task_id)

    return jsonify({"message": "Task deleted successfully"}), 200


# ============================================================
# RUN THE SERVER
# ============================================================
if __name__ == "__main__":
    # This block runs ONLY when you execute: python app.py
    # It does NOT run when another file imports app.py

    app.run(debug=True)
    # debug=True gives us:
    #   1. Auto-reload: server restarts when you save code changes
    #   2. Error pages: shows detailed errors in the browser
    # WARNING: Never use debug=True on a public server (security risk)
