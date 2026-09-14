# ============================================================
# app.py — The Main Entry Point of TaskFlow
# ============================================================
# This is the FIRST file that runs when you type: python app.py
# It creates the Flask app and defines ALL the routes (URLs).
# Think of it as the "receptionist" — it receives every request
# from the browser and decides what to do with it.
# ============================================================

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
# Flask         → The framework itself, creates our web app
# render_template → Turns HTML template files into web pages
# request       → Gives us access to data sent by the browser (form data, JSON, URL params)
# redirect      → Sends the browser to a different URL
# url_for       → Generates a URL from a function name (safer than hardcoding URLs)
# flash         → Shows a one-time message to the user (like "Task created!")
# jsonify       → Converts Python dictionaries to JSON responses for APIs

from database import init_db, get_all_users, get_user_by_id, create_user
from database import get_all_tasks, get_task_by_id, get_tasks_by_status
from database import create_task, update_task, delete_task
# We import all our database functions from database.py
# This keeps app.py clean — it doesn't need to know SQL

from models import user_to_dict, task_to_dict, VALID_STATUSES
# user_to_dict / task_to_dict → Convert database rows to dictionaries (for JSON)
# VALID_STATUSES → List of allowed statuses: ["pending", "in_progress", "completed"]

from forms import AddTaskForm, EditTaskForm, AddUserForm
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
# init_db() creates the users and tasks tables if they don't exist yet
# app_context() is needed because database operations require Flask to be "active"


# ============================================================
# HTML ROUTES — These return web pages that users see in the browser
# ============================================================
# Each route has:
#   @app.route("/some-url")  → What URL triggers this function
#   def function_name():     → The function that runs
#   return render_template() → Sends back an HTML page
# ============================================================


# --- Homepage ---
@app.route("/")
def home():
    """Show the homepage."""
    # render_template("index.html") reads templates/index.html,
    # processes any Jinja2 code inside it (like {{ }} and {% %}),
    # and returns the final HTML to the browser
    return render_template("index.html")


# --- List All Users ---
@app.route("/users")
def users():
    """Show a page with all users in a table."""
    all_users = get_all_users()  # Get all users from the database
    # Pass the users list to the template so it can display them
    # In the template, we access this as: {% for user in users %}
    return render_template("users.html", users=all_users)


# --- Add a New User (Form Page) ---
@app.route("/users/add", methods=["GET", "POST"])
def add_user():
    """
    Show the add user form (GET) or process the submitted form (POST).
    
    methods=["GET", "POST"] means this route handles BOTH:
      - GET  → User visits the page → Show the empty form
      - POST → User clicks Submit  → Process the form data
    """
    form = AddUserForm()  # Create a form instance

    # validate_on_submit() returns True ONLY when:
    #   1. The request is POST (form was submitted)
    #   2. All validation rules passed (name and email are not empty)
    #   3. CSRF token is valid (prevents fake submissions)
    if form.validate_on_submit():
        create_user(form.name.data, form.email.data)  # Save to database
        flash("User created successfully!", "success")  # Show success message
        return redirect(url_for("users"))  # Send browser to /users page
        # redirect + url_for = Post/Redirect/Get pattern
        # This prevents the form from being resubmitted if user refreshes the page

    # If GET request OR validation failed → show the form
    return render_template("add_user.html", form=form)


# --- List All Tasks (with optional status filter) ---
@app.route("/tasks")
def tasks():
    """
    Show all tasks. Supports filtering by status using query parameters.
    
    Examples:
      /tasks              → shows ALL tasks
      /tasks?status=pending → shows only pending tasks
    """
    # request.args.get("status") reads the ?status=xxx part from the URL
    # If there's no ?status= in the URL, it returns None
    status = request.args.get("status")

    if status and status in VALID_STATUSES:
        all_tasks = get_tasks_by_status(status)  # Get filtered tasks
    else:
        all_tasks = get_all_tasks()  # Get all tasks

    return render_template("tasks.html", tasks=all_tasks)


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
        # Extra check: make sure the user_id belongs to a real user
        user = get_user_by_id(form.user_id.data)
        if not user:
            flash("User ID does not exist. Create the user first.", "error")
            return render_template("add_task.html", form=form)

        # All checks passed → save the task
        create_task(
            form.title.data,        # Task title from the form
            form.description.data,  # Task description from the form
            form.status.data,       # Selected status from the dropdown
            form.user_id.data       # User ID from the form
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


# --- API: Create a User ---
@app.route("/api/users", methods=["POST"])
def api_create_user():
    """
    Create a new user via JSON.
    
    Expected JSON body:
      {"name": "Alice", "email": "alice@example.com"}
    """
    data = request.get_json()  # Read the JSON sent by the client

    # Validate: name and email must be present
    if not data or not data.get("name") or not data.get("email"):
        return jsonify({"error": "Name and email are required."}), 400
        # 400 = Bad Request (client sent wrong data)

    user_id = create_user(data["name"], data["email"])  # Save to database
    user = get_user_by_id(user_id)  # Fetch the newly created user

    return jsonify({
        "message": "User created successfully",
        "user": user_to_dict(user)  # Convert database row to dictionary
    }), 201  # 201 = Created (new resource was made)


# --- API: List All Users ---
@app.route("/api/users", methods=["GET"])
def api_get_users():
    """Return all users as a JSON list."""
    users = get_all_users()
    # Convert each user row to a dictionary, then return as JSON list
    return jsonify([user_to_dict(u) for u in users]), 200  # 200 = OK


# --- API: Get One User ---
@app.route("/api/users/<int:user_id>", methods=["GET"])
def api_get_user(user_id):
    """Return one user by ID as JSON."""
    user = get_user_by_id(user_id)

    if not user:
        return jsonify({"error": "User not found."}), 404  # 404 = Not Found

    return jsonify(user_to_dict(user)), 200


# --- API: Create a Task ---
@app.route("/api/tasks", methods=["POST"])
def api_create_task():
    """
    Create a new task via JSON.
    
    Expected JSON body:
      {"title": "Learn Flask", "description": "...", "status": "pending", "user_id": 1}
    """
    data = request.get_json()

    # Validate required fields
    if not data or not data.get("title") or not data.get("user_id"):
        return jsonify({"error": "Title and user_id are required."}), 400

    # Validate status (if provided)
    if data.get("status") and data["status"] not in VALID_STATUSES:
        return jsonify({"error": f"Invalid status. Use: {VALID_STATUSES}"}), 400

    # Check that the user exists
    user = get_user_by_id(data["user_id"])
    if not user:
        return jsonify({"error": "User not found."}), 404

    # Set default status to "pending" if not provided
    status = data.get("status", "pending")

    # Save to database
    task_id = create_task(data["title"], data.get("description", ""), status, data["user_id"])
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
