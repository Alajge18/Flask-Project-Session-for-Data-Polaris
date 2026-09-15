# Module 19 — Project Architecture

---

## Module 19 Syllabus Checklist

| # | Topic | Status |
|---|-------|--------|
| 1 | Project structure | Covered below |
| 2 | app.py responsibilities | Covered below |
| 3 | database.py responsibilities | Covered below |
| 4 | models.py responsibilities | Covered below |
| 5 | forms.py responsibilities | Covered below |
| 6 | Templates | Covered below |
| 7 | Static files | Covered below |
| 8 | requirements.txt | Covered below |
| 9 | Separation of responsibilities | Covered below |

---

## A. Concept Explanation — Why Separate Files?

### The Restaurant Analogy

A well-run restaurant has different people for different jobs:
- **Receptionist** → Greets customers, takes orders → `app.py`
- **Chef** → Cooks the food (handles data) → `database.py`
- **Quality checker** → Checks ingredients are fresh → `forms.py`
- **Menu designer** → Makes the menu look good → `templates/`
- **Interior designer** → Decorates the restaurant → `static/style.css`

If ONE person did everything, it would be chaos. The same applies to code.

### What is Separation of Concerns?

Each file has **ONE job**. If something breaks, you know exactly where to look:
- Form validation bug? → Check `forms.py`
- Database query wrong? → Check `database.py`
- Page looks broken? → Check `templates/` or `static/style.css`
- Wrong URL behavior? → Check `app.py`

---

## B. Complete Project Structure

```
TaskFlow/
│
├── app.py              ← Routes + request handling
├── database.py         ← SQLite operations
├── models.py           ← Data conversion helpers
├── forms.py            ← Form classes + validation
├── requirements.txt    ← Python package list
├── README.md           ← Project documentation
├── tasks.db            ← SQLite database file (auto-created)
│
├── templates/           ← HTML pages (Jinja2)
│   ├── base.html       ← Parent template (nav, flash messages)
│   ├── index.html      ← Homepage / Dashboard
│   ├── tasks.html      ← Task list + search + status filter
│   ├── add_task.html   ← Add task form (default: pending)
│   ├── task_detail.html← View one task
│   └── edit_task.html  ← Edit task form (update title, description, status)
│
├── static/              ← CSS, images, JavaScript
│   └── style.css       ← All styling
│
└── venv/                ← Virtual environment (don't edit)
```

---

## C. File-by-File Responsibilities

### [app.py](file:///c:/Users/chaud/Desktop/Projects/Data%20polaris/task%20management%20system%20by%20me/TaskFlow/app.py) — The Brain

| Responsibility | Example |
|---------------|---------|
| Creates the Flask app | `app = Flask(__name__)` |
| Sets configuration | `app.config["SECRET_KEY"] = "..."` |
| Initializes database | `init_db()` on startup |
| Defines HTML routes | `@app.route("/tasks")` |
| Defines search route | `@app.route("/tasks/search")` |
| Defines API routes | `@app.route("/api/tasks")` |
| Handles form submissions | `form.validate_on_submit()` |
| Returns HTML pages | `render_template("tasks.html", ...)` |
| Returns JSON responses | `jsonify({"message": "..."})` |
| Flash messages | `flash("Task created!", "success")` |
| Redirects | `redirect(url_for("tasks"))` |

### [database.py](file:///c:/Users/chaud/Desktop/Projects/Data%20polaris/task%20management%20system%20by%20me/TaskFlow/database.py) — The Storage

| Responsibility | Example |
|---------------|---------|
| Connects to SQLite | `sqlite3.connect("tasks.db")` |
| Creates tables | `CREATE TABLE IF NOT EXISTS ...` |
| Inserts data | `INSERT INTO tasks ...` |
| Reads data | `SELECT * FROM tasks` |
| Updates data | `UPDATE tasks SET ...` |
| Deletes data | `DELETE FROM tasks ...` |
| Counts data | `SELECT COUNT(*) FROM tasks` |
| Searches data | `WHERE title LIKE ? OR description LIKE ?` |
| Uses parameterized queries | `WHERE id = ?` with `(task_id,)` |

### [models.py](file:///c:/Users/chaud/Desktop/Projects/Data%20polaris/task%20management%20system%20by%20me/TaskFlow/models.py) — The Translator

| Responsibility | Example |
|---------------|---------|
| Converts task rows to dict | `task_to_dict(task)` |
| Defines valid statuses | `VALID_STATUSES = ["pending", ...]` |

### [forms.py](file:///c:/Users/chaud/Desktop/Projects/Data%20polaris/task%20management%20system%20by%20me/TaskFlow/forms.py) — The Validator

| Responsibility | Example |
|---------------|---------|
| Defines form fields | `title = StringField(...)` |
| Sets validation rules | `validators=[DataRequired()]` |
| CSRF protection | Automatic via `FlaskForm` |
| Error messages | `message="Title is required."` |

> **Note**: `AddTaskForm` has only `title` and `description` fields (no status dropdown).
> `EditTaskForm` includes the `status` SelectField so users can change status when editing.

### templates/ — The Face

| File | What it shows |
|------|--------------|
| `base.html` | Navigation bar + flash messages (shared by all pages) |
| `index.html` | Homepage with dashboard stats (color-coded stat cards) |
| `tasks.html` | Table of all tasks + search bar + filter links |
| `add_task.html` | Form to add a task (title + description only, status auto-set to pending) |
| `task_detail.html` | One task's full details |
| `edit_task.html` | Form to edit a task (title, description, and status dropdown) |

### static/style.css — The Appearance

Handles all visual styling: modern system fonts, clean blue buttons with hover animations, rounded stat cards with color-coded numbers, pill-shaped status badges, rounded tables, and responsive layouts.

### requirements.txt — The Shopping List

```
Flask==3.1.1
Flask-WTF==1.2.2
WTForms==3.2.1
```

Anyone can recreate your environment with `pip install -r requirements.txt`.

---

## D. How Files Communicate

```
BROWSER sends request
        ↓
   ┌─────────┐
   │  app.py  │ ← Receives request, decides what to do
   └────┬─────┘
        │
   ┌────┴──────────────────────────────────┐
   │                                       │
   ↓                                       ↓
┌──────────┐                        ┌──────────┐
│ forms.py │ validates form data    │database.py│ runs SQL queries
└──────────┘                        └─────┬────┘
                                          │
                                     ┌────┴───┐
                                     │tasks.db│ stores data
                                     └────────┘
        │
   ┌────┴──────────────────────────────────┐
   │                                       │
   ↓                                       ↓
┌───────────┐                       ┌──────────┐
│ templates/│ renders HTML pages    │ models.py│ converts data for JSON
└───────────┘                       └──────────┘
        │
        ↓
BROWSER receives response
```

### Example: Adding a Task via Form

```
1. Browser → GET /tasks/add → app.py
2. app.py creates AddTaskForm() from forms.py
3. app.py renders add_task.html from templates/
4. Browser shows the form

5. User fills form, clicks Submit
6. Browser → POST /tasks/add → app.py
7. app.py calls form.validate_on_submit() (forms.py checks rules)
8. If valid: app.py calls create_task() from database.py
9. database.py runs INSERT INTO tasks ... on tasks.db
10. app.py flashes "Task created!" and redirects to /tasks
```

### Example: Getting Tasks via API

```
1. API client → GET /api/tasks → app.py
2. app.py calls get_all_tasks() from database.py
3. database.py runs SELECT * FROM tasks on tasks.db
4. Returns rows to app.py
5. app.py calls task_to_dict() from models.py for each row
6. app.py returns jsonify(list_of_dicts) to API client
```

---

## E. Template Inheritance

```
base.html (parent)
├── Has: nav bar, flash messages, {% block content %}
│
├── index.html     → {% extends "base.html" %} → fills content block
├── tasks.html     → {% extends "base.html" %} → fills content block
├── add_task.html  → {% extends "base.html" %} → fills content block
├── task_detail.html → {% extends "base.html" %} → fills content block
└── edit_task.html → {% extends "base.html" %} → fills content block
```

**How it works:**

```html
<!-- base.html -->
<nav>...</nav>
{% block content %}{% endblock %}   ← This is a placeholder

<!-- tasks.html -->
{% extends "base.html" %}           ← Use base.html as parent
{% block content %}                 ← Fill in the placeholder
    <h1>All Tasks</h1>
    <table>...</table>
{% endblock %}

<!-- Result: base.html's nav + tasks.html's content = complete page -->
```

---

## F. Jinja2 Syntax Reference

| Syntax | What it does | Example |
|--------|-------------|---------|
| `{{ variable }}` | Print a value | `{{ task.title }}` |
| `{% if condition %}` | If statement | `{% if tasks %}` |
| `{% for item in list %}` | For loop | `{% for task in tasks %}` |
| `{% extends "file" %}` | Inherit from parent | `{% extends "base.html" %}` |
| `{% block name %}` | Define/fill a content block | `{% block content %}` |
| `{{ url_for('func') }}` | Generate URL | `{{ url_for('tasks') }}` → `/tasks` |
| `{{ form.field() }}` | Render form field | `{{ form.title(size=40) }}` |

---

## G. Common Mistakes and Fixes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Putting SQL in app.py | Code is messy, hard to maintain | Keep SQL in database.py |
| Skipping forms.py | No validation, security risks | Use Flask-WTF forms |
| Duplicating nav bar in every template | Hard to update | Use template inheritance (base.html) |
| Hardcoding URLs | Break if you rename routes | Use `url_for()` |
| Forgetting to import functions | `NameError` | Check imports at top of app.py |

---

## H. Practice Task

1. Look at each file in the project. Can you explain what each one does?
2. Trace the flow when a user adds a task: which files are involved in which order?
3. Add a new field to the tasks table (like `priority`). How many files need to change?
   - Hint: database.py (SQL), forms.py (form field), templates (display), app.py (handling)

---

## I. Teaching Questions

1. **"Why not put everything in app.py?"**
   - It would be too long and messy. Separating files makes code organized and easier to debug.

2. **"What does template inheritance mean?"**
   - Child templates extend a parent template. The parent has the common layout, children fill in specific content.

3. **"How does app.py talk to database.py?"**
   - By importing and calling functions: `from database import get_all_tasks`

4. **"What would break if we deleted models.py?"**
   - API routes would fail because they can't convert database rows to JSON dictionaries.

5. **"Why use `url_for('tasks')` instead of just writing `/tasks`?"**
   - If you rename the route URL later, `url_for` still works because it uses the function name, not the URL.

---

## J. Module 19 Completion Checklist

| # | Syllabus Point | Status | Demonstrated |
|---|---------------|--------|-------------|
| 1 | Project structure | Done | Full directory tree explained |
| 2 | app.py | Done | Routes, config, request handling |
| 3 | database.py | Done | SQLite connection, CRUD functions |
| 4 | models.py | Done | Data conversion, valid statuses |
| 5 | forms.py | Done | Flask-WTF form classes |
| 6 | Templates | Done | 6 templates with inheritance |
| 7 | Static files | Done | style.css for styling |
| 8 | requirements.txt | Done | Flask, Flask-WTF, WTForms |
| 9 | Separation of responsibilities | Done | Each file has one job |

**All 9 syllabus points for Module 19 are covered.**

> **Design Updates:**
> - `forms.py` → `AddTaskForm` no longer has a `status` dropdown — new tasks always start as `"pending"`
> - `app.py` → `add_task()` route hardcodes `"pending"` instead of reading `form.status.data`
> - `add_task.html` → Only shows Title and Description fields (no status dropdown)
> - `EditTaskForm` still has the status dropdown so users can change status when editing
> - `style.css` → Updated with modern buttons, color-coded stat cards, pill badges, rounded tables
> - `base.html` → CSS link includes `?v=2` for cache-busting
> - Task Search is implemented via `search_tasks()` in `database.py` and `/tasks/search` route in `app.py`

---

## K. Final Summary — All Modules Complete

| Module | Topic | Key File |
|--------|-------|----------|
| 10 | Introduction to Flask | app.py (basic) |
| 11 | Flask Routing | app.py (routes) |
| 12 | Query Parameters & Request Data | app.py (request object) |
| 13 | HTML Forms | templates/ |
| 14 | Flask-WTF | forms.py |
| 15 | APIs and JSON | app.py (API routes) |
| 16 | Database Fundamentals | database.py (schema) |
| 17 | SQL Basics | database.py (queries) |
| 18 | SQLite | database.py + tasks.db |
| 19 | Project Architecture | All files together |

**All modules (10–19) are fully implemented and documented.**
