# Module 15 — APIs and JSON

---

## Module 15 Syllabus Checklist

| # | Topic | Status |
|---|-------|--------|
| 1 | What an API is | Covered below |
| 2 | JSON request/response | Covered below |
| 3 | CRUD | Covered below |
| 4 | REST-style routes | Covered below |
| 5 | HTML Form vs API communication | Covered below |

---

## A. Concept Explanation — What is an API?

### The Waiter Analogy

Imagine a restaurant. You (the customer) can't go into the kitchen yourself. Instead, you tell the **waiter** what you want, and the waiter brings it to you.

An **API** (Application Programming Interface) is the waiter:
- **You** = a program (mobile app, Postman, another website)
- **The kitchen** = your Flask server + database
- **The waiter** = the API endpoints

### HTML Page vs API

| Feature | HTML Route | API Route |
|---------|-----------|-----------|
| **Returns** | Full HTML page | JSON data |
| **Used by** | Web browsers | Programs, mobile apps, Postman |
| **Response looks like** | A styled web page | `{"title": "Learn Flask", "status": "pending"}` |
| **Flask code** | `render_template(...)` | `jsonify(...)` |

---

## B. What is JSON?

JSON (JavaScript Object Notation) is a text format for structured data:

```json
{
    "id": 1,
    "title": "Learn Flask",
    "description": "Understand routes",
    "status": "pending"
}
```

- Looks like a Python dictionary
- Used everywhere on the internet for data exchange
- Human-readable and machine-readable

---

## C. What is CRUD?

CRUD = the four basic operations on data:

| Letter | Operation | HTTP Method | SQL | Example |
|--------|-----------|-------------|-----|---------|
| **C** | Create | POST | INSERT | Add a new task |
| **R** | Read | GET | SELECT | View tasks |
| **U** | Update | PUT | UPDATE | Change a task's status |
| **D** | Delete | DELETE | DELETE | Remove a task |

---

## D. All API Endpoints in TaskFlow

### Task API

| Method | URL | What it does | Status Code |
|--------|-----|-------------|-------------|
| POST | `/api/tasks` | Create a task | 201 Created |
| GET | `/api/tasks` | List all tasks | 200 OK |
| GET | `/api/tasks?status=pending` | Filter tasks | 200 OK |
| GET | `/api/tasks/<id>` | Get one task | 200 OK / 404 |
| PUT | `/api/tasks/<id>` | Update a task | 200 OK / 404 |
| DELETE | `/api/tasks/<id>` | Delete a task | 200 OK / 404 |

---

## E. Code Implementation

### Create a Task (POST)

```python
@app.route("/api/tasks", methods=["POST"])
def api_create_task():
    data = request.get_json()                    # Read JSON body
    if not data or not data.get("title"):
        return jsonify({"error": "Title is required."}), 400
    
    task_id = create_task(data["title"], data.get("description", ""), data.get("status", "pending"))
    task = get_task_by_id(task_id)
    return jsonify({
        "message": "Task created successfully",
        "task": task_to_dict(task)
    }), 201                                       # 201 = Created
```

```python
@app.route("/api/tasks", methods=["GET"])
def api_get_tasks():
    status = request.args.get("status")          # Optional filter
    if status:
        tasks = get_tasks_by_status(status)
    else:
        tasks = get_all_tasks()
    return jsonify([task_to_dict(t) for t in tasks]), 200
```

### Update a Task (PUT)

```python
@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def api_update_task(task_id):
    task = get_task_by_id(task_id)
    if not task:
        return jsonify({"error": "Task not found."}), 404
    
    data = request.get_json()
    title = data.get("title", task["title"])           # Keep old if not sent
    description = data.get("description", task["description"])
    status = data.get("status", task["status"])
    
    update_task(task_id, title, description, status)
    updated = get_task_by_id(task_id)
    return jsonify({
        "message": "Task updated successfully",
        "task": task_to_dict(updated)
    }), 200
```

### Delete a Task (DELETE)

```python
@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def api_delete_task(task_id):
    task = get_task_by_id(task_id)
    if not task:
        return jsonify({"error": "Task not found."}), 404
    delete_task(task_id)
    return jsonify({"message": "Task deleted successfully"}), 200
```

---

## F. HTTP Status Codes

| Code | Name | When to use |
|------|------|-------------|
| **200** | OK | Successful GET, PUT, DELETE |
| **201** | Created | Successful POST (new resource created) |
| **400** | Bad Request | Client sent invalid data (missing fields, bad status) |
| **404** | Not Found | Resource doesn't exist (wrong ID) |
| **500** | Internal Server Error | Bug in your code (unhandled exception) |

---

## G. Testing API Endpoints

### Using PowerShell curl:

```powershell
# Create a task
curl -X POST http://127.0.0.1:5000/api/tasks `
  -H "Content-Type: application/json" `
  -d '{"title": "Learn Flask", "status": "pending"}'

# Get all tasks
curl http://127.0.0.1:5000/api/tasks

# Update a task
curl -X PUT http://127.0.0.1:5000/api/tasks/1 `
  -H "Content-Type: application/json" `
  -d '{"status": "completed"}'

# Delete a task
curl -X DELETE http://127.0.0.1:5000/api/tasks/1
```

---

## H. Common Mistakes and Fixes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Forgetting `Content-Type: application/json` | `request.get_json()` returns None | Add the header in your API client |
| Not checking if data is None | `TypeError: 'NoneType'` | Always check `if not data:` |
| Returning 200 for creation | Misleading — 200 means "read" | Use 201 for POST (new resource) |
| Same function name as database function | Name collision | Use different names (e.g., `api_delete_task` vs `delete_task`) |

---

## I. Practice Task

1. Test all API endpoints using curl or Postman.
2. Try creating a task with missing `title` — observe the 400 error.
3. Try getting a task with ID 999 — observe the 404 error.

---

## J. Teaching Questions

1. **"What is the difference between a web page and an API?"**
   - Web page returns HTML for browsers. API returns JSON for programs.

2. **"What does CRUD stand for?"**
   - Create (POST), Read (GET), Update (PUT), Delete (DELETE).

3. **"Why do we use different HTTP methods (GET/POST/PUT/DELETE)?"**
   - Each method tells the server what operation to perform.

4. **"What is status code 201 vs 200?"**
   - 201 = new resource was created. 200 = request succeeded (generic).

5. **"Can the same URL have different behaviors for GET and POST?"**
   - Yes! `/api/tasks` with GET returns the list; with POST it creates a new task.

---

## K. Module 15 Completion Checklist

| # | Syllabus Point | Status | Demonstrated |
|---|---------------|--------|-------------|
| 1 | What an API is | Done | Waiter analogy + explanation |
| 2 | JSON request/response | Done | `request.get_json()` + `jsonify()` |
| 3 | CRUD | Done | All 4 operations for tasks |
| 4 | REST-style routes | Done | 6 endpoints with proper HTTP methods |
| 5 | HTML vs API | Done | Comparison table |

**All 5 syllabus points for Module 15 are covered.**
