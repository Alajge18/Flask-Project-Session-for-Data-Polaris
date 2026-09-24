"""
=============================================================================
MODULE 14: Form Validation with Flask-WTF
Project Story: Building our "Task Manager" Web App (Step 4)
=============================================================================
Previously in Module 13:
We built an HTML form, but checking for valid inputs manually is tedious.

Now in Module 14:
Flask-WTF allows us to define forms as Python Classes with built-in validation!
If a student enters an empty title or a title with only 1 letter,
Flask-WTF automatically blocks it and shows an error message.

What you will learn in this module:
1. Defining a form using FlaskForm
2. Adding validators (DataRequired, Length)
3. Using form.validate_on_submit() to check inputs
4. Displaying form validation errors to the user

Next Module Connection:
In Module 15, we will build a pure REST API returning JSON so mobile apps
and frontend frameworks can connect to our Task Manager!
=============================================================================
"""

from flask import Flask, render_template_string, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
app.config["SECRET_KEY"] = "simple_secret_key"

tasks = []

# =============================================================================
# 1. DEFINING THE FORM CLASS
# =============================================================================
class TaskForm(FlaskForm):
    # Title is required and must be at least 3 characters long
    title = StringField(
        "Task Title",
        validators=[
            DataRequired(message="Title cannot be empty!"),
            Length(min=3, message="Title must be at least 3 characters long!")
        ]
    )
    submit = SubmitField("Save Task")


# =============================================================================
# 2. INLINE HTML TEMPLATE WITH FORM ERRORS
# =============================================================================
FORM_PAGE = """
<!DOCTYPE html>
<html>
<body style="font-family: Arial; max-width: 450px; margin: 30px auto;">
    <h2>Add Task (with Flask-WTF Validation)</h2>

    <form method="POST">
        <!-- CSRF Token (Security handled by Flask-WTF) -->
        {{ form.hidden_tag() }}

        <p>
            {{ form.title.label }}<br>
            {{ form.title(size=30) }}
        </p>

        <!-- Display validation errors if any -->
        {% if form.title.errors %}
            {% for err in form.title.errors %}
                <p style="color: red;">⚠️ {{ err }}</p>
            {% endfor %}
        {% endif %}

        <p>{{ form.submit() }}</p>
    </form>
</body>
</html>
"""

# =============================================================================
# 3. ROUTE: VALIDATING FORM SUBMISSION
# =============================================================================
@app.route("/add-task", methods=["GET", "POST"])
def add_task():
    form = TaskForm()

    # validate_on_submit() returns True ONLY if method is POST and all rules pass!
    if form.validate_on_submit():
        new_task = {"id": len(tasks) + 1, "title": form.title.data}
        tasks.append(new_task)
        return f"<h3>Success! Task added: '{new_task['title']}'</h3>"

    return render_template_string(FORM_PAGE, form=form)


# =============================================================================
# RUNNING AND TESTING OUR CODE
# =============================================================================
if __name__ == "__main__":
    # Disable CSRF temporarily for our automated test client
    app.config["WTF_CSRF_ENABLED"] = False
    client = app.test_client()

    print("--- STEP 1: Submitting Invalid Input (Title too short) ---")
    r1 = client.post("/add-task", data={"title": "Go"})
    print("Caught error in HTML? ->", "Title must be at least 3 characters long!" in r1.data.decode("utf-8"))

    print("\n--- STEP 2: Submitting Valid Input ---")
    r2 = client.post("/add-task", data={"title": "Master Flask Forms"})
    print("Success response:", r2.data.decode("utf-8").strip())

    print("\n[NEXT STEP] In Module 15, we will build a pure JSON REST API!")
