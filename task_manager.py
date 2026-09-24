# ============================================================
# task_manager.py — Day 1: Python Task Manager (CLI Version)
# ============================================================
# This file covers Modules 1–6 of the workshop.
# It is a PURE PYTHON project — no Flask, no web, no database.
# Students build this FIRST, then convert it to Flask on Day 2.
#
# Modules Covered:
#   Module 1 — Functions and Scope
#   Module 2 — Modules and Packages
#   Module 3 — Object-Oriented Programming
#   Module 4 — Dictionaries and JSON Thinking
#   Module 5 — Decorators
#   Module 6 — Exception Handling
# ============================================================


# ============================================================
# MODULE 2 — Modules and Packages
# ============================================================
# 'import' brings in code from other files/libraries.
# Python has BUILT-IN modules (json, datetime) — no install needed.
# EXTERNAL packages (flask, flask-wtf) need: pip install <package>
#
# Later in Flask, we'll do:
#   from flask import Flask, request, jsonify
#   from flask_wtf import FlaskForm
#
# For now, we use Python's built-in modules:
# ============================================================

import json
# json module — converts Python dictionaries to JSON strings and back.
# This is the foundation for Flask's jsonify() function.

from datetime import datetime
# datetime module — gives us the current date and time.
# We use it to record when a task was created.


# ============================================================
# MODULE 6 — Exception Handling (Custom Exception)
# ============================================================
# Custom exceptions make error messages clear and specific.
# Instead of a generic "Error", we get "TaskNotFoundError".
#
# In Flask, we'll return HTTP 404 for "not found" errors.
# This is the Python equivalent of that concept.
# ============================================================

class TaskNotFoundError(Exception):
    """
    Custom exception raised when a task is not found.

    In Flask, this concept becomes:
        return jsonify({"error": "Task not found"}), 404
    """
    pass


class InvalidTaskDataError(Exception):
    """
    Custom exception raised when task data is invalid.

    In Flask, this concept becomes:
        return jsonify({"error": "Title is required"}), 400
    """
    pass


# ============================================================
# MODULE 5 — Decorators
# ============================================================
# A decorator is a function that WRAPS another function.
# It runs code BEFORE and AFTER the original function.
#
# Why does this matter for Flask?
# Flask uses decorators to connect URLs with functions:
#
#   @app.route("/tasks")     ← This is a decorator!
#   def get_tasks():
#       return "Tasks"
#
# The @app.route() decorator tells Flask:
# "When someone visits /tasks, run the get_tasks() function"
#
# Let's create our own decorator to understand how they work.
# ============================================================

def log_operation(func):
    """
    Decorator that logs when a function starts and finishes.

    How decorators work:
      1. log_operation receives the original function
      2. It creates a wrapper function
      3. The wrapper runs code BEFORE, calls the original, runs code AFTER
      4. It returns the wrapper (which replaces the original function)

    Usage:
      @log_operation
      def add_task(...):
          ...

    This is EXACTLY how Flask's @app.route() works internally!
    """
    def wrapper(*args, **kwargs):
        # *args and **kwargs allow the wrapper to accept ANY arguments
        # and pass them through to the original function.
        # (Module 1 — *args and **kwargs)
        print(f"\n>>> Starting: {func.__name__}()")
        result = func(*args, **kwargs)   # Call the original function
        print(f">>> Finished: {func.__name__}()")
        return result
    return wrapper


# ============================================================
# MODULE 3 — Object-Oriented Programming for Backend
# ============================================================
# Classes help us ORGANIZE related data and functions together.
#
# Without OOP:
#   task = {"id": 1, "title": "Learn Flask"}   ← just data
#   def update_task(task, title): ...           ← function is separate
#
# With OOP:
#   task = Task("Learn Flask")                  ← data + functions together
#   task.mark_complete()                        ← method belongs to the object
#
# In Flask, we'll use classes for:
#   - Form classes (Flask-WTF)
#   - Database models
#   - Configuration
# ============================================================

class Task:
    """
    Represents a single task.

    Module 3 Concepts:
      - __init__() → Constructor, runs when Task() is called
      - self → Refers to THIS specific task object
      - Instance attributes → Data that belongs to this task
      - Methods → Functions that belong to this task
      - Encapsulation → Task knows how to manage itself
    """

    def __init__(self, task_id, title, description="", status="pending"):
        """
        Initialize a new Task.

        Module 1 — Default Arguments:
          description="" and status="pending" have DEFAULT values.
          If you don't provide them, Python uses the defaults.

          Task(1, "Learn Flask")                    → description="", status="pending"
          Task(1, "Learn Flask", "Read the docs")   → description="Read the docs", status="pending"
          Task(1, "Learn Flask", status="completed") → description="", status="completed"
        """
        # --- Instance Attributes (Module 3) ---
        # These belong to THIS specific task object (self)
        self.id = task_id
        self.title = title
        self.description = description
        self.status = status                         # "pending", "in_progress", "completed"
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # strftime() formats the date as a string: "2025-01-15 14:30:00"

    def mark_complete(self):
        """
        Mark this task as completed.

        Module 3 — Methods:
          A method is a function that belongs to a class.
          It always takes 'self' as the first parameter.
          'self' refers to THIS specific task.
        """
        self.status = "completed"

    def to_dict(self):
        """
        Convert this Task to a Python dictionary.

        Module 4 — Dictionaries and JSON Thinking:
          This is the BRIDGE between Python objects and JSON.

          Python Dictionary ↔ JSON

          In Flask, when we return JSON from an API:
            return jsonify(task.to_dict())

          The dictionary looks like:
            {"id": 1, "title": "Learn Flask", "status": "pending"}

          And JSON looks EXACTLY the same! That's the connection.
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at
        }

    def __str__(self):
        """
        String representation of the task (for printing).

        When you do print(task), Python calls this method.
        """
        return f"[{self.status.upper()}] {self.title} (ID: {self.id})"


# ============================================================
# MODULE 3 — TaskManager Class (Encapsulation)
# ============================================================
# TaskManager ENCAPSULATES all task operations.
# The outside world doesn't need to know HOW tasks are stored.
# It just calls methods like add_task(), get_all_tasks(), etc.
#
# This is the same pattern we'll use in Flask:
#   app.py calls database.py functions
#   app.py doesn't need to know SQL
# ============================================================

class TaskManager:
    """
    Manages all tasks — Add, View, Update, Delete, Search.

    Module 3 — Encapsulation:
      The _tasks list is 'private' (starts with _).
      Other code should use methods, not access _tasks directly.
      This protects the data from being changed incorrectly.
    """

    def __init__(self):
        """Initialize with an empty task list and a counter for IDs."""
        self._tasks = []          # Private list — use methods to access
        self._next_id = 1         # Auto-incrementing ID (like database AUTOINCREMENT)

    # ============================================================
    # MODULE 1 — Functions and Scope
    # ============================================================
    # Each method below demonstrates:
    #   - Function parameters (task_id, title, etc.)
    #   - Return values (return the created/updated task)
    #   - Variable scope (self._tasks is instance scope, local vars are function scope)
    # ============================================================

    @log_operation    # ← Module 5: Decorator applied!
    def add_task(self, title, description="", **kwargs):
        """
        Add a new task.

        Module 1 — **kwargs:
          **kwargs collects any EXTRA keyword arguments into a dictionary.
          Example: add_task("Learn", priority="high", tags=["python"])
          kwargs would be: {"priority": "high", "tags": ["python"]}

          We don't use them here, but this shows the concept.
          In Flask, **kwargs is used in many places.

        Module 6 — Exception Handling:
          We validate the input and raise an exception if invalid.
        """
        # --- Module 6: Input Validation with Exception Handling ---
        try:
            if not title or not title.strip():
                raise InvalidTaskDataError("Task title is required.")
                # This is like returning HTTP 400 Bad Request in Flask

            # Create the task
            task = Task(self._next_id, title.strip(), description.strip())
            self._tasks.append(task)
            self._next_id += 1

            # Show extra kwargs if any were passed (Module 1 — **kwargs demo)
            if kwargs:
                print(f"   Extra options received: {kwargs}")

            print(f"   ✓ Task created: {task}")
            return task

        except InvalidTaskDataError as e:
            # Module 6: Catching specific exceptions
            print(f"   ✗ Validation Error: {e}")
            return None

    def get_all_tasks(self):
        """
        Get all tasks.

        Module 1 — Return Values:
          This function RETURNS a list of tasks.
          The caller receives this list and can use it.

        Module 4 — Dictionary Thinking:
          We return dictionaries (not Task objects) because
          JSON APIs need dictionaries, not Python objects.
        """
        return [task.to_dict() for task in self._tasks]
        # List comprehension: creates a new list by calling to_dict() on each task

    def get_task_by_id(self, task_id):
        """
        Find a task by its ID.

        Module 6 — Exception Handling:
          If the task doesn't exist, we raise TaskNotFoundError.
          In Flask, this becomes: return jsonify({"error": "Not found"}), 404
        """
        for task in self._tasks:
            if task.id == task_id:
                return task

        # Task not found — raise an exception
        raise TaskNotFoundError(f"Task with ID {task_id} not found.")

    @log_operation
    def update_task(self, task_id, title=None, description=None, status=None):
        """
        Update a task's title, description, or status.

        Module 1 — Default Arguments:
          All parameters have default value None.
          Only the provided values get updated.
          This is like a PUT request in Flask where you only
          send the fields you want to change.
        """
        try:
            task = self.get_task_by_id(task_id)

            # Only update fields that were provided (not None)
            if title is not None:
                if not title.strip():
                    raise InvalidTaskDataError("Title cannot be empty.")
                task.title = title.strip()

            if description is not None:
                task.description = description.strip()

            if status is not None:
                valid_statuses = ["pending", "in_progress", "completed"]
                if status not in valid_statuses:
                    raise InvalidTaskDataError(
                        f"Invalid status '{status}'. Use: {valid_statuses}"
                    )
                task.status = status

            print(f"   ✓ Task updated: {task}")
            return task

        except TaskNotFoundError as e:
            print(f"   ✗ Error: {e}")
            return None
        except InvalidTaskDataError as e:
            print(f"   ✗ Validation Error: {e}")
            return None

    @log_operation
    def delete_task(self, task_id):
        """
        Delete a task by ID.

        Module 6 — Exception Handling:
          try/except catches the error if task doesn't exist.
          finally runs whether success or failure.
        """
        try:
            task = self.get_task_by_id(task_id)
            self._tasks.remove(task)
            print(f"   ✓ Task deleted: {task}")
            return True

        except TaskNotFoundError as e:
            print(f"   ✗ Error: {e}")
            return False

        finally:
            # Module 6 — finally:
            # This block ALWAYS runs, whether success or error.
            # Useful for cleanup operations (closing files, database connections).
            print(f"   (Delete operation for ID {task_id} completed)")

    @log_operation
    def mark_task_complete(self, task_id):
        """Mark a task as completed."""
        try:
            task = self.get_task_by_id(task_id)
            task.mark_complete()
            print(f"   ✓ Task completed: {task}")
            return task
        except TaskNotFoundError as e:
            print(f"   ✗ Error: {e}")
            return None

    def get_tasks_by_status(self, status):
        """
        Filter tasks by status.

        Module 1 — Function Parameters:
          'status' is a required parameter (no default value).
          The caller MUST provide it.

        This is the Python version of:
          GET /tasks?status=pending
        which we'll build in Flask on Day 3.
        """
        return [
            task.to_dict() for task in self._tasks
            if task.status == status
        ]

    def search_tasks(self, query):
        """
        Search tasks by title or description.

        This is the Python version of:
          GET /tasks/search?q=flask
        which we'll build in Flask on Day 3.
        """
        query_lower = query.lower()
        return [
            task.to_dict() for task in self._tasks
            if query_lower in task.title.lower()
            or query_lower in task.description.lower()
        ]

    def get_task_counts(self):
        """
        Get counts of tasks by status.

        Module 4 — Dictionaries:
          Returns a dictionary that looks like:
          {"total": 5, "pending": 2, "in_progress": 1, "completed": 2}

          In Flask, this dictionary becomes JSON automatically:
          return jsonify(counts)
        """
        return {
            "total": len(self._tasks),
            "pending": len([t for t in self._tasks if t.status == "pending"]),
            "in_progress": len([t for t in self._tasks if t.status == "in_progress"]),
            "completed": len([t for t in self._tasks if t.status == "completed"])
        }


# ============================================================
# MODULE 4 — Dictionaries and JSON Thinking (Demo Function)
# ============================================================

def show_json_thinking():
    """
    Demonstrate the Python Dictionary ↔ JSON relationship.

    This is THE KEY CONCEPT for REST APIs:
      Python Dictionary → json.dumps() → JSON String
      JSON String → json.loads() → Python Dictionary

    In Flask:
      return jsonify({"id": 1, "title": "Learn Flask"})
      # Flask does json.dumps() internally and sets Content-Type: application/json
    """
    print("\n" + "=" * 60)
    print("MODULE 4 — Dictionaries and JSON Thinking")
    print("=" * 60)

    # A Python dictionary
    task = {
        "id": 1,
        "title": "Learn Flask",
        "description": "Study Flask framework",
        "status": "pending"
    }
    print(f"\nPython Dictionary:\n  {task}")
    print(f"  Type: {type(task)}")

    # Convert to JSON string
    json_string = json.dumps(task, indent=2)
    print(f"\nJSON String:\n{json_string}")
    print(f"  Type: {type(json_string)}")

    # Convert back to dictionary
    back_to_dict = json.loads(json_string)
    print(f"\nBack to Dictionary:\n  {back_to_dict}")
    print(f"  Type: {type(back_to_dict)}")

    # A list of dictionaries (like an API response)
    tasks_list = [
        {"id": 1, "title": "Learn Flask", "status": "pending"},
        {"id": 2, "title": "Build API", "status": "in_progress"},
        {"id": 3, "title": "Deploy App", "status": "completed"}
    ]
    print(f"\nAPI Response (list of tasks):")
    print(json.dumps(tasks_list, indent=2))
    print("\n  → This is exactly what GET /api/tasks returns in Flask!")


# ============================================================
# MODULE 5 — Decorators Deep Dive (Demo Function)
# ============================================================

def show_decorator_to_flask_bridge():
    """
    Show how decorators connect to Flask's @app.route().

    Step 1: We create a simple decorator
    Step 2: We show how Flask uses the SAME concept
    """
    print("\n" + "=" * 60)
    print("MODULE 5 — Decorators → Flask Bridge")
    print("=" * 60)

    # --- Simple decorator example ---
    def my_decorator(func):
        def wrapper():
            print("  [Before function runs]")
            func()
            print("  [After function runs]")
        return wrapper

    @my_decorator
    def say_hello():
        print("  Hello, World!")

    print("\nUsing @my_decorator:")
    say_hello()

    # --- How Flask uses decorators ---
    print("\n--- Flask Connection ---")
    print("""
    In Flask, @app.route("/tasks") works the SAME WAY:

    @app.route("/tasks")      ← Decorator: registers this URL
    def get_tasks():           ← Function: runs when URL is visited
        return "Tasks"         ← Response: sent back to browser

    The decorator tells Flask:
    "When someone visits /tasks, run the get_tasks() function"
    """)


# ============================================================
# MODULE 1 — *args and **kwargs Demo
# ============================================================

def print_task_info(*args, **kwargs):
    """
    Demonstrate *args and **kwargs.

    *args:   Collects extra POSITIONAL arguments into a tuple
    **kwargs: Collects extra KEYWORD arguments into a dictionary

    Module 1 — Variable Scope:
      'args' and 'kwargs' are LOCAL to this function.
      They cannot be accessed outside this function.
      This is called FUNCTION SCOPE.
    """
    print("\n--- *args and **kwargs Demo ---")
    print(f"  Positional args (*args): {args}")
    print(f"  Keyword args (**kwargs): {kwargs}")

    for arg in args:
        print(f"    - {arg}")

    for key, value in kwargs.items():
        print(f"    - {key}: {value}")


# ============================================================
# MAIN PROGRAM — Interactive Task Manager CLI
# ============================================================
# This is the "Practical Task" for Day 1.
# Students run this and interact with the menu.
# ============================================================

def main():
    """
    Main function — runs the interactive Task Manager.

    Module 1 — Variable Scope:
      'manager' is a LOCAL variable — it only exists inside main().
      The functions above are GLOBAL — they can be used anywhere.
    """
    print("=" * 60)
    print("   TaskFlow — Python Task Manager (Day 1)")
    print("   Modules 1-6: Functions, OOP, Decorators, Exceptions")
    print("=" * 60)

    # --- Module 5: Decorator → Flask Bridge Demo ---
    show_decorator_to_flask_bridge()

    # --- Module 4: JSON Thinking Demo ---
    show_json_thinking()

    # --- Module 1: *args and **kwargs Demo ---
    print_task_info("Task 1", "Task 2", priority="high", category="learning")

    # --- Create Task Manager ---
    manager = TaskManager()

    # Add some sample tasks
    print("\n" + "=" * 60)
    print("CREATING SAMPLE TASKS")
    print("=" * 60)
    manager.add_task("Learn Python Basics", "Study variables, loops, functions")
    manager.add_task("Learn Flask", "Study Flask framework for web development")
    manager.add_task("Build REST API", "Create CRUD endpoints")
    manager.add_task("Learn SQLite", "Study database operations")
    manager.add_task("Deploy to Render", "Push to GitHub and deploy")

    # --- Interactive Menu ---
    while True:
        print("\n" + "-" * 40)
        print("  TASK MANAGER MENU")
        print("-" * 40)
        print("  1. View All Tasks")
        print("  2. View Task by ID")
        print("  3. Add New Task")
        print("  4. Update Task")
        print("  5. Delete Task")
        print("  6. Mark Task Complete")
        print("  7. Filter by Status")
        print("  8. Search Tasks")
        print("  9. View Task Counts")
        print("  10. View as JSON")
        print("  0. Exit")
        print("-" * 40)

        choice = input("  Choose an option: ").strip()

        # ============================================================
        # MODULE 6 — Exception Handling in Action
        # ============================================================
        # Every menu option is wrapped in try/except.
        # This prevents the program from crashing on bad input.
        # In Flask, we do the same: validate input, return errors.
        # ============================================================

        try:
            if choice == "1":
                # View all tasks
                tasks = manager.get_all_tasks()
                if not tasks:
                    print("\n  No tasks found.")
                else:
                    print(f"\n  All Tasks ({len(tasks)}):")
                    for t in tasks:
                        status_icon = {"pending": "⏳", "in_progress": "🔄", "completed": "✅"}
                        icon = status_icon.get(t["status"], "❓")
                        print(f"    {icon} [{t['id']}] {t['title']} — {t['status']}")

            elif choice == "2":
                # View single task
                task_id = int(input("  Enter Task ID: "))
                task = manager.get_task_by_id(task_id)
                print(f"\n  Task Details:")
                print(f"    ID:          {task.id}")
                print(f"    Title:       {task.title}")
                print(f"    Description: {task.description or 'No description'}")
                print(f"    Status:      {task.status}")
                print(f"    Created:     {task.created_at}")

            elif choice == "3":
                # Add task
                title = input("  Task Title: ")
                description = input("  Description (optional): ")
                manager.add_task(title, description)

            elif choice == "4":
                # Update task
                task_id = int(input("  Task ID to update: "))
                print("  (Press Enter to skip a field)")
                title = input("  New Title: ").strip() or None
                description = input("  New Description: ").strip() or None
                status = input("  New Status (pending/in_progress/completed): ").strip() or None
                manager.update_task(task_id, title=title, description=description, status=status)

            elif choice == "5":
                # Delete task
                task_id = int(input("  Task ID to delete: "))
                manager.delete_task(task_id)

            elif choice == "6":
                # Mark complete
                task_id = int(input("  Task ID to complete: "))
                manager.mark_task_complete(task_id)

            elif choice == "7":
                # Filter by status
                status = input("  Status (pending/in_progress/completed): ").strip()
                tasks = manager.get_tasks_by_status(status)
                if not tasks:
                    print(f"\n  No {status} tasks found.")
                else:
                    print(f"\n  {status.upper()} Tasks ({len(tasks)}):")
                    for t in tasks:
                        print(f"    [{t['id']}] {t['title']}")

            elif choice == "8":
                # Search
                query = input("  Search query: ").strip()
                results = manager.search_tasks(query)
                if not results:
                    print(f"\n  No tasks matching '{query}'.")
                else:
                    print(f"\n  Search Results for '{query}' ({len(results)}):")
                    for t in results:
                        print(f"    [{t['id']}] {t['title']} — {t['status']}")

            elif choice == "9":
                # Task counts
                counts = manager.get_task_counts()
                print(f"\n  Task Counts:")
                print(f"    Total:       {counts['total']}")
                print(f"    Pending:     {counts['pending']}")
                print(f"    In Progress: {counts['in_progress']}")
                print(f"    Completed:   {counts['completed']}")

            elif choice == "10":
                # View as JSON (Module 4)
                tasks = manager.get_all_tasks()
                print(f"\n  JSON Output (this is what an API returns):")
                print(json.dumps(tasks, indent=2))

            elif choice == "0":
                print("\n  Goodbye! 👋")
                print("  Next step: Convert this to a Flask web application (Day 2)")
                break

            else:
                print("  Invalid choice. Try again.")

        except TaskNotFoundError as e:
            # Module 6: Specific exception for missing tasks
            print(f"\n  ✗ Not Found: {e}")

        except ValueError:
            # Module 6: Catches invalid number input (e.g., "abc" instead of "1")
            print("\n  ✗ Invalid input. Please enter a number.")

        except Exception as e:
            # Module 6: Catch-all for unexpected errors
            print(f"\n  ✗ Unexpected Error: {e}")


# ============================================================
# MODULE 1 — Variable Scope: __name__ check
# ============================================================
# __name__ is a GLOBAL variable set by Python.
# When you RUN this file directly:   __name__ == "__main__"
# When you IMPORT this file:         __name__ == "task_manager"
#
# This pattern ensures main() only runs when you execute:
#   python task_manager.py
# It does NOT run if another file does:
#   from task_manager import TaskManager
#
# Flask uses the EXACT same pattern:
#   if __name__ == "__main__":
#       app.run(debug=True)
# ============================================================

if __name__ == "__main__":
    main()
