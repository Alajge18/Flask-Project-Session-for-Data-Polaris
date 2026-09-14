# Module 12 — Query Parameters & Request Data

---

## Module 12 Syllabus Checklist

| # | Topic | Status |
|---|-------|--------|
| 1 | Query parameters | Covered below |
| 2 | `request.args` | Covered below |
| 3 | `request.form` | Covered below |
| 4 | `request.json` | Covered below |
| 5 | When to use each type | Covered below |

---

## A. Concept Explanation — How Does Data Reach Flask?

### The Mail Analogy

Think of sending a letter. There are three ways to send information:

1. **Write on the envelope** (everyone can see it) → Query Parameters
2. **Put it inside the envelope** (hidden, for forms) → Form Data
3. **Send a digital message** (structured data) → JSON Data

Flask can receive data in all three ways. Each has a different use case.

---

## B. The Three Ways to Send Data

### 1. Query Parameters — Data in the URL

The data appears **after a `?`** in the URL:

```
http://127.0.0.1:5000/tasks?status=pending
                            ^^^^^^^^^^^^^^^^
                            This is the query parameter
```

- `status` is the **key**
- `pending` is the **value**

**When to use**: Filtering, searching, pagination. Data is visible in the URL.

**How to read in Flask**:
```python
from flask import request

@app.route("/tasks")
def tasks():
    status = request.args.get("status")
    # URL: /tasks?status=pending  →  status = "pending"
    # URL: /tasks                 →  status = None
```

**TaskFlow example** — Filtering tasks by status:
```python
@app.route("/tasks")
def tasks():
    status = request.args.get("status")  # Read ?status=xxx from URL
    
    if status and status in VALID_STATUSES:
        all_tasks = get_tasks_by_status(status)  # Filtered list
    else:
        all_tasks = get_all_tasks()  # All tasks
    
    return render_template("tasks.html", tasks=all_tasks)
```

**URLs to test**:
```
/tasks                    → Shows ALL tasks
/tasks?status=pending     → Shows only pending tasks
/tasks?status=completed   → Shows only completed tasks
/tasks?status=in_progress → Shows only in-progress tasks
```

---

### 2. Form Data — Data from HTML Forms

When a user fills out a form and clicks Submit, the data is sent in the **request body** (not visible in the URL).

**When to use**: Adding or editing data through web pages.

**How to read in Flask** (raw way):
```python
@app.route("/tasks/add", methods=["POST"])
def add_task():
    title = request.form.get("title")
    description = request.form.get("description")
```

**How to read in Flask** (Flask-WTF way — what we use):
```python
@app.route("/tasks/add", methods=["GET", "POST"])
def add_task():
    form = AddTaskForm()
    if form.validate_on_submit():
        title = form.title.data          # Same as request.form.get("title")
        description = form.description.data  # But with validation!
```

> We use Flask-WTF instead of raw `request.form` because it adds validation and CSRF protection. More on this in Module 14.

---

### 3. JSON Data — Data from API Clients

When a program (not a browser) sends data, it usually sends **JSON** (JavaScript Object Notation):

```json
{
    "title": "Learn Flask",
    "description": "Understand routes",
    "status": "pending"
}
```

**When to use**: API communication (mobile apps, Postman, curl, other programs).

**How to read in Flask**:
```python
@app.route("/api/tasks", methods=["POST"])
def api_create_task():
    data = request.get_json()  # Parse the JSON body
    
    title = data.get("title")        # "Learn Flask"
    description = data.get("description")  # "Understand routes"
    status = data.get("status")      # "pending"
```

**TaskFlow example** — Creating a task via API:
```python
@app.route("/api/tasks", methods=["POST"])
def api_create_task():
    data = request.get_json()
    
    # Validate required fields
    if not data or not data.get("title"):
        return jsonify({"error": "Title is required."}), 400
    
    # Save to database
    task_id = create_task(
        data["title"],
        data.get("description", ""),    # Default to empty string
        data.get("status", "pending")   # Default to "pending"
    )
    
    task = get_task_by_id(task_id)
    return jsonify({
        "message": "Task created successfully",
        "task": task_to_dict(task)
    }), 201
```

---

## C. Comparison Table

| Feature | Query Parameters | Form Data | JSON Data |
|---------|-----------------|-----------|-----------|
| **Where data travels** | In the URL after `?` | In the request body | In the request body |
| **Visible in URL?** | Yes | No | No |
| **HTTP method** | Usually GET | Usually POST | POST, PUT, DELETE |
| **Flask code** | `request.args.get("key")` | `request.form.get("key")` | `request.get_json()` |
| **Used by** | Browsers (links, filters) | HTML forms | API clients (Postman, apps) |
| **Use case** | Filtering, searching | Adding/editing via web | API communication |
| **Content-Type** | N/A | `application/x-www-form-urlencoded` | `application/json` |

---

## D. Execution Flow

### Query Parameter Flow (`/tasks?status=pending`)

```
1. User clicks "Pending" filter link on the tasks page
2. Browser sends: GET /tasks?status=pending
3. Flask matches @app.route("/tasks")
4. Flask calls tasks() function
5. Inside tasks(): request.args.get("status") returns "pending"
6. get_tasks_by_status("pending") queries the database
7. Template renders only pending tasks
8. Browser shows filtered task list
```

### JSON API Flow (`POST /api/tasks`)

```
1. API client sends: POST /api/tasks with JSON body
2. Flask matches @app.route("/api/tasks", methods=["POST"])
3. Flask calls api_create_task() function
4. Inside: data = request.get_json() reads the JSON
5. Validation checks: title and user_id present?
6. create_task() saves to database
7. Flask returns JSON response with status 201
8. API client receives the response
```

---

## E. Testing Query Parameters

In your browser, try these URLs:

```
http://127.0.0.1:5000/tasks                    → All tasks
http://127.0.0.1:5000/tasks?status=pending     → Only pending
http://127.0.0.1:5000/tasks?status=completed   → Only completed
http://127.0.0.1:5000/tasks?status=in_progress → Only in progress
```

Testing the API (PowerShell):

```powershell
# Create a task via JSON
curl -X POST http://127.0.0.1:5000/api/tasks `
  -H "Content-Type: application/json" `
  -d '{"title": "Test Task", "status": "pending"}'

# Get all tasks via API
curl http://127.0.0.1:5000/api/tasks

# Filter via API
curl "http://127.0.0.1:5000/api/tasks?status=pending"
```

---

## F. Common Mistakes and Fixes

| Mistake | Problem | Fix |
|---------|---------|-----|
| `request.args.get("status")` on a POST form | Gets URL params, not form data | Use `request.form.get()` or Flask-WTF |
| `request.form.get("title")` on a JSON API | Gets form data, not JSON | Use `request.get_json()` |
| Forgetting `methods=["POST"]` | Flask only accepts GET by default | Add `methods=["GET", "POST"]` |
| Not checking if `data` is None | `request.get_json()` returns None if no JSON sent | Always check: `if not data:` |
| Using `.get("key")` vs `["key"]` | `["key"]` crashes if key missing | `.get("key")` returns None safely |

---

## G. Practice Task

1. Test the API by creating a task with curl or Postman, then retrieving it.
2. Try filtering tasks by status using query parameters.

---

## H. Teaching Questions

1. **"What's the difference between `request.args` and `request.form`?"**
   - `request.args` reads data from the URL (after `?`). `request.form` reads data from a submitted HTML form body.

2. **"When would you use query parameters vs JSON?"**
   - Query parameters for filtering/searching (GET requests). JSON for creating/updating data (POST/PUT requests).

3. **"What does `request.get_json()` return if no JSON is sent?"**
   - Returns `None`. That's why we always check `if not data:`.

4. **"Why is form data not visible in the URL but query parameters are?"**
   - Form data (POST) is sent in the request body. Query parameters (GET) are appended to the URL.

5. **"Can you have both query parameters AND a JSON body in the same request?"**
   - Yes! Example: `POST /api/tasks?debug=true` with a JSON body. Use `request.args` for the URL part and `request.get_json()` for the body.

---

## I. Module 12 Completion Checklist

| # | Syllabus Point | Status | Demonstrated |
|---|---------------|--------|-------------|
| 1 | Query parameters | Done | `/tasks?status=pending` |
| 2 | `request.args` | Done | `request.args.get("status")` |
| 3 | `request.form` | Done | Explained, used via Flask-WTF |
| 4 | `request.json` | Done | `request.get_json()` in API routes |
| 5 | When to use each | Done | Comparison table |

**All 5 syllabus points for Module 12 are covered.**
