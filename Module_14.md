# Module 14 — Flask-WTF (Form Validation)

---

## Module 14 Syllabus Checklist

| # | Topic | Status |
|---|-------|--------|
| 1 | Flask-WTF | Covered below |
| 2 | WTForms | Covered below |
| 3 | Form classes | Covered below |
| 4 | Fields | Covered below |
| 5 | Validators / DataRequired | Covered below |
| 6 | CSRF protection | Covered below |
| 7 | Validation errors | Covered below |

---

## A. Concept Explanation — Why Flask-WTF?

### The Bouncer Analogy

Imagine a nightclub with a bouncer at the door. The bouncer checks everyone's ID before letting them in. If your ID is fake or you're underage, you're turned away.

**Flask-WTF is like a bouncer for your forms:**
- It checks every piece of data before letting it into your application.
- Empty title? Rejected.
- Invalid user ID? Rejected.
- Missing CSRF token? Rejected.

### Manual vs Flask-WTF Validation

**Without Flask-WTF** (manual — messy and error-prone):
```python
@app.route("/tasks/add", methods=["POST"])
def add_task():
    title = request.form.get("title")
    if not title:
        flash("Title is required!", "error")
        return redirect(url_for("add_task"))
    if not request.form.get("user_id"):
        flash("User ID is required!", "error")
        return redirect(url_for("add_task"))
    # ... more manual checks ...
```

**With Flask-WTF** (clean and automatic):
```python
@app.route("/tasks/add", methods=["GET", "POST"])
def add_task():
    form = AddTaskForm()
    if form.validate_on_submit():  # All checks happen automatically!
        create_task(form.title.data, ...)
```

---

## B. SECRET_KEY — Why It's Needed

```python
app.config["SECRET_KEY"] = "my-secret-key-for-learning"
```

Flask-WTF uses the SECRET_KEY to create CSRF tokens. Without it, forms won't work.

**What is CSRF?**
- Cross-Site Request Forgery — a hacker tricks your browser into submitting a form to your app from a fake website.
- CSRF tokens prevent this: each form gets a unique, secret token that only your server can verify.
- `{{ form.hidden_tag() }}` adds this token to the form HTML.

---

## C. Code Implementation — forms.py

### [forms.py](file:///c:/Users/chaud/Desktop/Projects/Data%20polaris/task%20management%20system%20by%20me/TaskFlow/forms.py):

```python
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired


class AddTaskForm(FlaskForm):
    """Form to add a new task. Status is NOT included — new tasks always start as pending."""
    title = StringField("Title", validators=[
        DataRequired(message="Title is required.")
    ])
    description = TextAreaField("Description")
    # No status field — new tasks automatically go to "pending"
    submit = SubmitField("Add Task")


class EditTaskForm(FlaskForm):
    """Form to edit an existing task. Includes status dropdown so users can change it."""
    title = StringField("Title", validators=[
        DataRequired(message="Title is required.")
    ])
    description = TextAreaField("Description")
    status = SelectField("Status", choices=[
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed")
    ])
    submit = SubmitField("Update Task")
```

> **Design Decision**: The Add form intentionally omits the status dropdown.
> New tasks should always start as "pending" — the user only picks a status when editing later.

---

## D. Field Types Reference

| Field Type | HTML Element | Used In |
|-----------|-------------|--------|
| `StringField` | `<input type="text">` | Title (Add + Edit) |
| `TextAreaField` | `<textarea>` | Description (Add + Edit) |
| `SelectField` | `<select>` dropdown | Status (**Edit only**) |
| `SubmitField` | `<button type="submit">` | Add Task, Update Task |

---

## E. Validators Reference

| Validator | What it checks | Example |
|-----------|---------------|---------|
| `DataRequired()` | Field is not empty | `DataRequired(message="Title is required.")` |
| `NumberRange(min, max)` | Number is within range | `NumberRange(min=1)` |
| `Length(min, max)` | Text length is within range | `Length(min=2, max=100)` |
| `Email()` | Text looks like an email | `Email()` (needs `email-validator` package) |
| `EqualTo(field)` | Two fields match | `EqualTo("password")` for confirm password |

---

## F. How validate_on_submit() Works

```python
form.validate_on_submit()
```

This returns `True` ONLY when ALL three conditions are met:

| Check | What it verifies |
|-------|-----------------|
| 1. Is it POST? | The form was actually submitted (not just displayed) |
| 2. Validators passed? | All field rules are satisfied (title not empty, etc.) |
| 3. CSRF token valid? | The hidden token matches what the server generated |

If ANY check fails, it returns `False` and the form's `.errors` dictionary is populated.

---

## G. Displaying Validation Errors

In the template:
```html
<div class="form-group">
    {{ form.title.label }}
    {{ form.title(size=40) }}
    {% for error in form.title.errors %}
        <span class="error">{{ error }}</span>
    {% endfor %}
</div>
```

When the user submits with an empty title:
- `form.title.errors` = `["Title is required."]`
- The error message shows in red below the field

---

## H. Pre-filling Forms (Edit Page)

When editing a task, the form should show the **current** values:

```python
@app.route("/tasks/<int:task_id>/edit", methods=["GET", "POST"])
def edit_task(task_id):
    task = get_task_by_id(task_id)
    form = EditTaskForm()
    
    if form.validate_on_submit():
        update_task(task_id, form.title.data, form.description.data, form.status.data)
        flash("Task updated!", "success")
        return redirect(url_for("task_detail", task_id=task_id))
    
    # Pre-fill the form on GET request
    if request.method == "GET":
        form.title.data = task["title"]           # Fill title field
        form.description.data = task["description"]  # Fill description
        form.status.data = task["status"]          # Select current status
    
    return render_template("edit_task.html", form=form, task=task)
```

---

## I. Common Mistakes and Fixes

| Mistake | Error | Fix |
|---------|-------|-----|
| No SECRET_KEY | RuntimeError about missing secret key | Set `app.config["SECRET_KEY"]` |
| Forgot `{{ form.hidden_tag() }}` | Form submits but validation always fails | Add hidden_tag inside `<form>` |
| Wrong field type | IntegerField shows text error on letters | Use correct field type for data |
| Not showing errors in template | User doesn't know why form failed | Loop through `form.field.errors` |
| Not pre-filling edit form | Edit page shows empty fields | Set `form.field.data` on GET |

---

## J. Practice Task

1. Add a `Length(min=3)` validator to the task title so titles must be at least 3 characters.
2. Try submitting a task with a 1-character title and observe the error.

---

## K. Teaching Questions

1. **"Why use Flask-WTF instead of checking `request.form` manually?"**
   - Flask-WTF is cleaner, automatic, reusable, and includes CSRF protection.

2. **"What is CSRF and why do we need protection?"**
   - CSRF = a hacker tricks your browser into submitting a form. The CSRF token proves the form came from your own website.

3. **"What does `DataRequired()` do?"**
   - It checks that the field is not empty. If empty, validation fails and an error message is shown.

4. **"What's the difference between `validate_on_submit()` and just checking `request.method == 'POST'`?"**
   - `validate_on_submit()` checks POST + validators + CSRF. Just checking POST skips validation entirely.

5. **"How do you pre-fill a form for editing?"**
   - Set `form.field.data = existing_value` on GET requests.

---

## L. Module 14 Completion Checklist

| # | Syllabus Point | Status | Demonstrated |
|---|---------------|--------|-------------|
| 1 | Flask-WTF | Done | `FlaskForm` base class used |
| 2 | WTForms | Done | All field types imported from wtforms |
| 3 | Form classes | Done | `AddTaskForm` (no status), `EditTaskForm` (with status) |
| 4 | Fields | Done | StringField, TextAreaField, SelectField (edit only) |
| 5 | Validators / DataRequired | Done | DataRequired |
| 6 | CSRF protection | Done | SECRET_KEY + hidden_tag() |
| 7 | Validation errors | Done | Error display in templates |

**All 7 syllabus points for Module 14 are covered.**
