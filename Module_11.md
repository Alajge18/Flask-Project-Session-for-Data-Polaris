# Module 11 — Flask Routing

---

## Module 11 Syllabus Checklist

| # | Topic | Status |
|---|-------|--------|
| 1 | Static routes | Covered below |
| 2 | Dynamic routes | Covered below |
| 3 | URL parameters | Covered below |
| 4 | Route converters | Covered below |
| 5 | `@app.route()` | Covered below |

---

## A. Concept Explanation — What is Routing?

### The Restaurant Analogy

Imagine a restaurant with a reception desk. When a customer says "I want Table 5," the receptionist looks at the table map and guides them to the right table.

**Flask routing works the same way:**
- The **customer** is the web browser.
- The **request** ("I want Table 5") is the URL (`/tasks/5`).
- The **receptionist** is Flask's routing system.
- The **table** is the Python function that handles that URL.

### What is a Route?

A **route** is a rule that connects a **URL** to a **Python function**.

```
URL Path        →  Python Function  →  What the user sees
─────────────────────────────────────────────────────────
/               →  home()           →  Welcome message
/about          →  about()          →  About page text
/tasks          →  tasks()          →  List of all tasks
/tasks/3        →  task_detail(3)   →  Details of task #3
```

---

## B. Static Routes vs Dynamic Routes

### Static Routes — The URL never changes

```python
@app.route("/")          # Always exactly "/"
@app.route("/about")     # Always exactly "/about"
@app.route("/tasks")     # Always exactly "/tasks"
```

> **Analogy**: A static route is like a labeled drawer. "Forks" always has forks.

### Dynamic Routes — Part of the URL is a variable

```python
@app.route("/tasks/<int:task_id>")    # /tasks/1, /tasks/2, /tasks/99
@app.route("/hello/<name>")           # /hello/Alice, /hello/Bob
```

The `< >` part captures whatever appears in that position.

> **Analogy**: A dynamic route is like a mail slot labeled "Apartment `<number>`."

---

## C. Code Implementation

### Static Route Example — Homepage

```python
@app.route("/")
def home():
    return render_template("index.html")
```

| Concept | Explanation |
|---------|-------------|
| URL | `/` (the homepage) |
| Type | Static — always exactly `/` |
| Response | Renders the index.html template |

### Static Route Example — Task List

```python
@app.route("/tasks")
def tasks():
    status = request.args.get("status")
    if status and status in VALID_STATUSES:
        all_tasks = get_tasks_by_status(status)
    else:
        all_tasks = get_all_tasks()
    return render_template("tasks.html", tasks=all_tasks)
```

### Dynamic Route — Task Detail with `int` Converter

```python
@app.route("/tasks/<int:task_id>")
def task_detail(task_id):
    task = get_task_by_id(task_id)
    if not task:
        flash("Task not found.", "error")
        return redirect(url_for("tasks"))
    return render_template("task_detail.html", task=task)
```

#### `<int:task_id>` — What does this mean?

| Part | Meaning |
|------|---------|
| `< >` | Variable part of the URL |
| `int:` | Converter — only accepts integers |
| `task_id` | Variable name — becomes a function parameter |

#### How it works:

```
URL visited    →  What Flask does              →  task_id value
/tasks/1       →  Converts "1" to integer 1    →  task_id = 1
/tasks/99      →  Converts "99" to integer 99  →  task_id = 99
/tasks/abc     →  "abc" is NOT an integer!     →  Flask returns 404 automatically
```

### Dynamic Route — Edit Task

```python
@app.route("/tasks/<int:task_id>/edit", methods=["GET", "POST"])
def edit_task(task_id):
    task = get_task_by_id(task_id)
    if not task:
        flash("Task not found.", "error")
        return redirect(url_for("tasks"))
    # ... form handling ...
```

This shows you can have **multiple segments** in a dynamic URL: `/tasks/3/edit`.

---

## D. Route Converters — Reference Table

| Converter | Accepts | Example | Python type |
|-----------|---------|---------|-------------|
| `string` (default) | Any text without `/` | `/hello/Alice` | `str` |
| `int` | Positive integers | `/tasks/42` | `int` |
| `float` | Decimal numbers | `/price/9.99` | `float` |
| `path` | Text including `/` | `/files/docs/readme.txt` | `str` |

---

## E. How Flask Chooses the Correct Route

```
Request: GET /tasks/3

Flask checks each route:
  @app.route("/")                    → no match → SKIP
  @app.route("/users")              → no match → SKIP
  @app.route("/tasks")              → "/tasks/3" != "/tasks" → SKIP
  @app.route("/tasks/<int:task_id>") → MATCH! "3" converts to int → Run task_detail(3)
```

`/tasks` and `/tasks/3` are **different routes** handled by different functions.

---

## F. All Routes in TaskFlow

| URL | Type | Method | Function | What it does |
|-----|------|--------|----------|-------------|
| `/` | Static | GET | `home()` | Homepage |
| `/users` | Static | GET | `users()` | List users |
| `/users/add` | Static | GET/POST | `add_user()` | Add user form |
| `/tasks` | Static | GET | `tasks()` | List tasks |
| `/tasks/add` | Static | GET/POST | `add_task()` | Add task form |
| `/tasks/<int:task_id>` | Dynamic | GET | `task_detail()` | View one task |
| `/tasks/<int:task_id>/edit` | Dynamic | GET/POST | `edit_task()` | Edit task form |
| `/tasks/<int:task_id>/delete` | Dynamic | GET | `delete_task_route()` | Delete a task |

---

## G. Common Mistakes and Fixes

| Mistake | Error | Fix |
|---------|-------|-----|
| Missing function parameter | `TypeError: got unexpected argument` | Add `task_id` parameter to function |
| Parameter name mismatch | `TypeError` | URL `<task_id>` must match function `def f(task_id)` |
| Two functions same name | Second overwrites first | Every function needs a unique name |
| Not returning status code | Error shows as 200 OK | Use `return "Not found", 404` |
| Trailing slash confusion | 404 on `/about/` | Define as `/about` (without slash) |

---

## H. Practice Task

1. Add a route `/tasks/<int:task_id>/status` that returns only the status of a task.
2. Add a route `/users/<int:user_id>/tasks` that returns all tasks for a specific user.
3. Test in your browser.

---

## I. Teaching Questions

1. **"Difference between `/tasks` and `/tasks/3`?"**
   - `/tasks` is static (all tasks). `/tasks/3` is dynamic (one task).

2. **"What does `<int:task_id>` do? What if someone visits `/tasks/hello`?"**
   - Only accepts integers. `/tasks/hello` returns 404 automatically.

3. **"Why return 404 when task not found?"**
   - Without 404, browser thinks request succeeded (200 OK).

4. **"Can two routes point to the same function?"**
   - Yes, stack multiple `@app.route()` decorators.

5. **"Difference between `<name>` and `<int:task_id>`?"**
   - `<name>` accepts any text. `<int:task_id>` only accepts integers.

---

## J. Module 11 Completion Checklist

| # | Syllabus Point | Status | Demonstrated |
|---|---------------|--------|-------------|
| 1 | Static routes | Done | `/`, `/about`, `/tasks`, `/users` |
| 2 | Dynamic routes | Done | `/tasks/<int:task_id>`, etc. |
| 3 | URL parameters | Done | `task_id`, `user_id` in routes |
| 4 | Route converters | Done | `int:`, `string` (default) |
| 5 | `@app.route()` | Done | Used in all routes |

**All 5 syllabus points for Module 11 are covered.**
