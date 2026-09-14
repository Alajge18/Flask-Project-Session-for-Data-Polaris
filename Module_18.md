# Module 18 — SQLite

---

## Module 18 Syllabus Checklist

| # | Topic | Status |
|---|-------|--------|
| 1 | What SQLite is | Covered below |
| 2 | Creating tasks.db | Covered below |
| 3 | Users and Tasks tables | Covered below |
| 4 | User-Task relationship | Covered below |
| 5 | Flask + SQLite architecture | Covered below |
| 6 | Database persistence | Covered below |

---

## A. Concept Explanation — What is SQLite?

### The Notebook Analogy

Most databases (MySQL, PostgreSQL) are like a **secretary** — a separate person (server) that you talk to whenever you need data. You have to set them up, keep them running, and pay for them.

**SQLite** is like a **notebook**. It's a single file on your computer. No server needed. You just open it, read/write, and close it.

### Key Facts

| Feature | SQLite |
|---------|--------|
| **Storage** | Single file (`tasks.db`) |
| **Server needed?** | No (it's embedded) |
| **Python support** | Built-in (`import sqlite3`) |
| **Good for** | Small-medium apps, learning, prototyping |
| **Used by** | Android apps, iOS apps, browsers, many websites |

---

## B. Code Implementation — database.py

The complete [database.py](file:///c:/Users/chaud/Desktop/Projects/Data%20polaris/task%20management%20system%20by%20me/TaskFlow/database.py):

### Connecting to the Database

```python
import sqlite3

DATABASE = "tasks.db"

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
```

**Line-by-line:**

| Line | What it does | Why |
|------|-------------|-----|
| `sqlite3.connect(DATABASE)` | Opens the database file (creates it if it doesn't exist) | Every operation needs a connection |
| `conn.row_factory = sqlite3.Row` | Makes rows accessible by column name | `row["name"]` instead of `row[1]` |
| `PRAGMA foreign_keys = ON` | Enables foreign key enforcement | SQLite disables them by default |

### Key Concepts

#### Connection

A **connection** is like a phone call to the database. You open it, talk (run queries), and close it.

```python
conn = get_db()      # Pick up the phone
# ... do stuff ...
conn.close()         # Hang up
```

#### Cursor

A **cursor** is the tool that executes SQL commands and returns results.

```python
cursor = conn.execute("SELECT * FROM users")  # Run the SQL
rows = cursor.fetchall()                       # Get the results
```

Most of the time, `conn.execute()` creates a cursor automatically.

#### commit()

`commit()` saves your changes to the database file permanently.

```python
conn.execute("INSERT INTO users ...")
conn.commit()   # Without this, the INSERT is NOT saved!
conn.close()
```

**Rule**: Always `commit()` after INSERT, UPDATE, or DELETE. SELECT doesn't need commit.

#### close()

`close()` releases the database connection. Like hanging up a phone.

```python
conn.close()  # Free up resources
```

---

### Creating Tables

```python
def init_db():
    conn = get_db()
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL DEFAULT 'pending',
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    conn.commit()
    conn.close()
```

This runs when the app starts:
```python
# In app.py:
with app.app_context():
    init_db()
```

---

### CRUD Helper Functions

```python
# CREATE
def create_user(name, email):
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO users (name, email) VALUES (?, ?)",
        (name, email)
    )
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id

# READ (all)
def get_all_tasks():
    conn = get_db()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return tasks

# READ (one)
def get_task_by_id(task_id):
    conn = get_db()
    task = conn.execute(
        "SELECT * FROM tasks WHERE id = ?", (task_id,)
    ).fetchone()
    conn.close()
    return task

# READ (filtered)
def get_tasks_by_status(status):
    conn = get_db()
    tasks = conn.execute(
        "SELECT * FROM tasks WHERE status = ?", (status,)
    ).fetchall()
    conn.close()
    return tasks

# UPDATE
def update_task(task_id, title, description, status):
    conn = get_db()
    conn.execute(
        "UPDATE tasks SET title = ?, description = ?, status = ? WHERE id = ?",
        (title, description, status, task_id)
    )
    conn.commit()
    conn.close()

# DELETE
def delete_task(task_id):
    conn = get_db()
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
```

---

## C. Database Persistence — Why Data Stays

When you stop the Flask server (`Ctrl+C`), your data is NOT lost. Here's why:

```
Flask server (app.py)     ←→     tasks.db file (on hard drive)
    ↓ (server stops)              ↓ (file stays)
  GONE                          STILL THERE
```

- `tasks.db` is a **file on your hard drive** — just like a Word document.
- Flask just reads/writes to this file.
- Stopping Flask doesn't delete the file.
- Next time you run `python app.py`, it reconnects to the same file.

---

## D. How Flask Routes Call Database Functions

```
Browser request → app.py route → database.py function → tasks.db
                                                        ↓
Browser display ← app.py template ← database.py result ←
```

Example — Viewing all tasks:

```python
# Step 1: Browser visits /tasks
# Step 2: Flask calls this route:
@app.route("/tasks")
def tasks():
    all_tasks = get_all_tasks()   # Step 3: Call database.py function
    return render_template("tasks.html", tasks=all_tasks)  # Step 4: Send to template

# Step 3 inside database.py:
def get_all_tasks():
    conn = get_db()                                        # Connect to tasks.db
    tasks = conn.execute("SELECT * FROM tasks").fetchall()  # Run SQL
    conn.close()                                           # Disconnect
    return tasks                                           # Return results
```

---

## E. Common Mistakes and Fixes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Forgetting `conn.commit()` | Data not saved to file | Always commit after INSERT/UPDATE/DELETE |
| Forgetting `conn.close()` | Connection leak | Always close after you're done |
| Not enabling foreign keys | Invalid user_id allowed | Add `PRAGMA foreign_keys = ON` |
| Forgetting `row_factory = sqlite3.Row` | Can't access columns by name | Set it in `get_db()` |
| Passing wrong number of `?` values | `ProgrammingError` | Count `?` must match tuple length |

---

## F. Practice Task

1. Open Python terminal and manually insert a user:
   ```python
   import sqlite3
   conn = sqlite3.connect("tasks.db")
   conn.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("Charlie", "c@test.com"))
   conn.commit()
   print(conn.execute("SELECT * FROM users").fetchall())
   conn.close()
   ```
2. Restart the Flask server and verify Charlie appears on the Users page.
3. This proves: data persists even when the server is off.

---

## G. Teaching Questions

1. **"What is SQLite? How is it different from MySQL?"**
   - SQLite = single file, no server. MySQL = separate server process.

2. **"What does `commit()` do?"**
   - Saves changes permanently to the database file.

3. **"Why do we close connections?"**
   - To free resources. Too many open connections can cause problems.

4. **"What happens to data when the Flask server stops?"**
   - Nothing! Data is in the file. Server just reads/writes to it.

5. **"What is `row_factory = sqlite3.Row`?"**
   - Lets you access columns by name (`row["name"]`) instead of index (`row[1]`).

---

## H. Module 18 Completion Checklist

| # | Syllabus Point | Status | Demonstrated |
|---|---------------|--------|-------------|
| 1 | What SQLite is | Done | Single-file database, no server |
| 2 | Creating tasks.db | Done | Auto-created by `sqlite3.connect()` |
| 3 | Users and Tasks tables | Done | `init_db()` with CREATE TABLE |
| 4 | User-Task relationship | Done | Foreign key in tasks table |
| 5 | Flask + SQLite architecture | Done | Route → database function → SQL |
| 6 | Database persistence | Done | Data stays after server stops |

**All 6 syllabus points for Module 18 are covered.**
