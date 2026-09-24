"""
=============================================================================
MODULE 13: HTML Forms and Jinja2 Templates
Project Story: Building our "Task Manager" Web App (Step 3)
=============================================================================
Previously in Module 12:
We accepted form inputs, but writing HTML inside Python strings was messy.

Now in Module 13:
Flask uses the Jinja2 templating engine to render dynamic HTML pages.
You can pass Python variables directly into HTML templates!

What you will learn in this module:
1. {{ variable }} -> Printing variables in HTML
2. {% for task in tasks %} -> Looping through our task list in HTML
3. {% if condition %} -> Showing different styles or badges
4. flash() -> Showing a success banner when a task is added

Next Module Connection:
In Module 14, we will use Flask-WTF to automatically validate our form inputs
and prevent empty submissions!
=============================================================================
"""

from flask import Flask, request, render_template_string, redirect, url_for, flash

app = Flask(__name__)
# Flask requires a secret_key to enable flash messages
app.secret_key = "beginner_secret_key"

tasks = [
    {"id": 1, "title": "Setup Flask Project", "status": "Completed"},
    {"id": 2, "title": "Design Jinja2 Layout", "status": "In Progress"}
]

# =============================================================================
# SIMPLE JINJA2 HTML TEMPLATE (All in one file for easy learning)
# =============================================================================
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Task Manager</title>
</head>
<body style="font-family: Arial; max-width: 500px; margin: 30px auto;">
    <h2>My Task Manager</h2>

    <!-- Flash message display -->
    {% with messages = get_flashed_messages() %}
        {% if messages %}
            {% for msg in messages %}
                <p style="color: green; background: #e0f8e0; padding: 8px;">{{ msg }}</p>
            {% endfor %}
        {% endif %}
    {% endwith %}

    <!-- Loop through tasks using Jinja2 -->
    <h3>Tasks ({{ tasks|length }})</h3>
    <ul>
    {% for task in tasks %}
        <li>
            <strong>{{ task.title }}</strong> - 
            {% if task.status == 'Completed' %}
                <span style="color: green;">Done</span>
            {% else %}
                <span style="color: orange;">Pending</span>
            {% endif %}
        </li>
    {% endfor %}
    </ul>

    <!-- HTML Form to add a new task -->
    <hr>
    <h3>Add a Task</h3>
    <form method="POST" action="/tasks">
        <input type="text" name="title" placeholder="Enter task title" required>
        <button type="submit">Add Task</button>
    </form>
</body>
</html>
"""

# =============================================================================
# ROUTE: RENDERING THE TEMPLATE & HANDLING FORM SUBMISSION
# =============================================================================
@app.route("/tasks", methods=["GET", "POST"])
def manage_tasks():
    if request.method == "POST":
        title = request.form.get("title")
        if title:
            tasks.append({"id": len(tasks) + 1, "title": title, "status": "Pending"})
            flash("Task added successfully!")
        return redirect(url_for("manage_tasks"))

    # GET request: render the template and pass the tasks list
    return render_template_string(HTML_PAGE, tasks=tasks)


# =============================================================================
# RUNNING AND TESTING OUR CODE
# =============================================================================
if __name__ == "__main__":
    client = app.test_client()

    print("--- STEP 1: Rendering the Jinja2 Page ---")
    r1 = client.get("/tasks")
    print("Page status code:", r1.status_code)

    print("\n--- STEP 2: Submitting a Task via Form ---")
    r2 = client.post("/tasks", data={"title": "Test Jinja Task"}, follow_redirects=True)
    print("Contains new task? ->", "Test Jinja Task" in r2.data.decode("utf-8"))

    print("\n[NEXT STEP] In Module 14, we will use Flask-WTF to validate forms easily!")
