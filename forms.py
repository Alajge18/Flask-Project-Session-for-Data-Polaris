# ============================================================
# forms.py — Flask-WTF Form Classes
# ============================================================
# This file defines our HTML forms using Flask-WTF and WTForms.
#
# Why use Flask-WTF instead of plain HTML forms?
#   1. Validation: Automatically checks if fields are filled correctly
#   2. CSRF Protection: Prevents fake form submissions from other websites
#   3. Error Messages: Shows helpful error messages next to fields
#   4. Reusable: One form class can be used for add AND edit pages
#
# How it works:
#   1. We define a form class with fields and rules (validators)
#   2. In app.py, we create a form instance: form = AddTaskForm()
#   3. In the template, we render it: {{ form.title() }}
#   4. When submitted, Flask-WTF checks all rules automatically
# ============================================================

from flask_wtf import FlaskForm
# FlaskForm is the base class for all our forms
# It adds CSRF protection automatically

from wtforms import StringField, TextAreaField, SelectField, SubmitField
# StringField    → A single-line text input (<input type="text">)
# TextAreaField  → A multi-line text input (<textarea>)
# SelectField    → A dropdown menu (<select>)
# SubmitField    → A submit button (<input type="submit">)

from wtforms.validators import DataRequired
# DataRequired → The field cannot be empty (must have a value)


class AddTaskForm(FlaskForm):
    """
    Form to add a new task.
    
    Fields:
      - title: Required text field for the task name
      - description: Optional text area for details
      - status: Dropdown with three choices
      - submit: The submit button
    """
    title = StringField(
        "Title",  # The label shown next to the field
        validators=[DataRequired(message="Title is required.")]
        # DataRequired() means: if this field is empty, show the error message
    )

    description = TextAreaField(
        "Description"
        # No validators → this field is optional
    )

    status = SelectField(
        "Status",
        choices=[
            ("pending", "Pending"),           # (value_saved, text_displayed)
            ("in_progress", "In Progress"),   # "in_progress" is saved to database
            ("completed", "Completed")        # "Completed" is shown to the user
        ],
        validators=[DataRequired()]
    )

    submit = SubmitField("Add Task")
    # This creates the submit button with the text "Add Task"


class EditTaskForm(FlaskForm):
    """
    Form to edit an existing task.
    
    Same fields as AddTaskForm — title, description, and status.
    """
    title = StringField(
        "Title",
        validators=[DataRequired(message="Title is required.")]
    )

    description = TextAreaField("Description")

    status = SelectField(
        "Status",
        choices=[
            ("pending", "Pending"),
            ("in_progress", "In Progress"),
            ("completed", "Completed")
        ],
        validators=[DataRequired()]
    )

    submit = SubmitField("Update Task")
