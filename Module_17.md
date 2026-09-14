# Module 17 — SQL Basics

---

## Module 17 Syllabus Checklist

| # | Topic | Status |
|---|-------|--------|
| 1 | CREATE | Covered below |
| 2 | INSERT | Covered below |
| 3 | SELECT | Covered below |
| 4 | UPDATE | Covered below |
| 5 | DELETE | Covered below |

---

## A. Concept Explanation — What is SQL?

### The Librarian Analogy

Imagine you're in a library. You can't just grab books yourself — you talk to the librarian:

- "**Create** a new shelf called 'Science'" → `CREATE TABLE`
- "**Add** this book to the Science shelf" → `INSERT INTO`
- "**Find** all science books" → `SELECT`
- "**Change** this book's author" → `UPDATE`
- "**Remove** this book" → `DELETE`

**SQL** (Structured Query Language) is the language you use to talk to a database. It has 5 essential commands.

---

## B. The 5 SQL Commands

### 1. CREATE TABLE — Make a new table

```sql
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Word by word:**

| SQL | Meaning |
|-----|---------|
| `CREATE TABLE` | Make a new table |
| `IF NOT EXISTS` | Only if it doesn't already exist (safe to run multiple times) |
| `tasks` | The table name |
| `id INTEGER` | Column named "id" that stores whole numbers |
| `PRIMARY KEY` | This column uniquely identifies each row |
| `AUTOINCREMENT` | Automatically assign the next number (1, 2, 3...) |
| `title TEXT` | Column named "title" that stores text |
| `NOT NULL` | This column cannot be empty |
| `DEFAULT 'pending'` | If no status is given, use 'pending' |
| `DEFAULT CURRENT_TIMESTAMP` | Auto-fill with the current date and time |

**Python code in [database.py](file:///c:/Users/chaud/Desktop/Projects/Data%20polaris/task%20management%20system%20by%20me/TaskFlow/database.py):**

```python
def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
```

---

### 2. INSERT INTO — Add a new row

```sql
INSERT INTO tasks (title, description, status) VALUES ('Learn Flask', 'Understand routes', 'pending');
```

**Word by word:**

| SQL | Meaning |
|-----|---------|
| `INSERT INTO tasks` | Add a new row to the tasks table |
| `(title, description, status)` | We're filling these columns |
| `VALUES ('Learn Flask', ...)` | With these values |

Note: We don't specify `id` because `AUTOINCREMENT` fills it automatically.

**Python code:**

```python
def create_task(title, description, status):
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO tasks (title, description, status) VALUES (?, ?, ?)",
        (title, description, status)
    )
    conn.commit()
    task_id = cursor.lastrowid  # Get the auto-generated ID
    conn.close()
    return task_id
```

**Why `?` instead of putting values directly?**

```python
# DANGEROUS — SQL Injection attack possible!
conn.execute(f"INSERT INTO tasks (title) VALUES ('{title}')")
# A hacker could set title to: '); DROP TABLE tasks; --
# This would DELETE your entire tasks table!

# SAFE — Parameterized query
conn.execute("INSERT INTO tasks (title, description, status) VALUES (?, ?, ?)", (title, description, status))
# The ? placeholders are safely escaped. No injection possible.
```

---

### 3. SELECT — Read/find data

```sql
-- Get ALL tasks
SELECT * FROM tasks;

-- Get one task by ID
SELECT * FROM tasks WHERE id = 1;

-- Get only pending tasks
SELECT * FROM tasks WHERE status = 'pending';

-- Get specific columns only
SELECT title, status FROM tasks;

-- Get tasks ordered by newest first
SELECT * FROM tasks ORDER BY id DESC;
```

**Word by word:**

| SQL | Meaning |
|-----|---------|
| `SELECT *` | Get ALL columns |
| `FROM tasks` | From the tasks table |
| `WHERE id = 1` | Only rows where id equals 1 |
| `ORDER BY id DESC` | Sort by id, newest first |

**Python code:**

```python
# Get all tasks
def get_all_tasks():
    conn = get_db()
    tasks = conn.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
    # .fetchall() returns a list of ALL matching rows
    conn.close()
    return tasks

# Get one task
def get_task_by_id(task_id):
    conn = get_db()
    task = conn.execute(
        "SELECT * FROM tasks WHERE id = ?", (task_id,)
    ).fetchone()
    # .fetchone() returns ONE row (or None if not found)
    conn.close()
    return task
```

---

### 4. UPDATE — Change existing data

```sql
UPDATE tasks SET status = 'completed' WHERE id = 1;
```

**Word by word:**

| SQL | Meaning |
|-----|---------|
| `UPDATE tasks` | Change rows in the tasks table |
| `SET status = 'completed'` | Set the status column to 'completed' |
| `WHERE id = 1` | Only for the row where id is 1 |

**IMPORTANT**: Always use `WHERE`! Without it, ALL rows get updated:
```sql
UPDATE tasks SET status = 'completed';  -- THIS UPDATES EVERY TASK!
```

**Python code:**

```python
def update_task(task_id, title, description, status):
    conn = get_db()
    conn.execute(
        "UPDATE tasks SET title = ?, description = ?, status = ? WHERE id = ?",
        (title, description, status, task_id)
    )
    conn.commit()  # Must commit to save changes!
    conn.close()
```

---

### 5. DELETE — Remove a row

```sql
DELETE FROM tasks WHERE id = 1;
```

**Word by word:**

| SQL | Meaning |
|-----|---------|
| `DELETE FROM tasks` | Remove rows from the tasks table |
| `WHERE id = 1` | Only the row where id is 1 |

**IMPORTANT**: Always use `WHERE`! Without it, ALL rows get deleted:
```sql
DELETE FROM tasks;  -- THIS DELETES EVERY TASK!
```

**Python code:**

```python
def delete_task(task_id):
    conn = get_db()
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
```

---

## C. SQL Command Summary

| Command | What it does | Example |
|---------|-------------|---------|
| `CREATE TABLE` | Make a new table | `CREATE TABLE tasks (...)` |
| `INSERT INTO` | Add a row | `INSERT INTO tasks VALUES (...)` |
| `SELECT` | Read rows | `SELECT * FROM tasks WHERE id = 1` |
| `UPDATE` | Change a row | `UPDATE tasks SET status = 'done' WHERE id = 1` |
| `DELETE` | Remove a row | `DELETE FROM tasks WHERE id = 1` |

---

## D. Common Mistakes and Fixes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Forgetting `conn.commit()` | Changes are not saved | Always call `commit()` after INSERT/UPDATE/DELETE |
| Missing `WHERE` in UPDATE/DELETE | Changes ALL rows! | Always specify which row to change |
| Using f-strings for SQL values | SQL injection vulnerability | Use `?` placeholders |
| Forgetting the comma in `(task_id,)` | Python error — not a tuple | Single-element tuples need a trailing comma |
| Not closing connection | Resource leak | Always call `conn.close()` |

---

## E. Practice Task

1. Open a Python terminal and connect to tasks.db:
   ```python
   import sqlite3
   conn = sqlite3.connect("tasks.db")
   conn.row_factory = sqlite3.Row
   ```
2. Run `SELECT * FROM tasks` and print the results.
3. Insert a new task with SQL, then select all tasks to verify.
4. Update a task's status and verify with SELECT.

---

## F. Teaching Questions

1. **"What does SELECT * FROM tasks mean?"**
   - Get all columns from all rows in the tasks table.

2. **"Why do we use ? instead of putting values directly in SQL?"**
   - To prevent SQL injection attacks. `?` is safely escaped by SQLite.

3. **"What happens if you forget WHERE in a DELETE statement?"**
   - ALL rows in the table get deleted!

4. **"What does `commit()` do? What happens without it?"**
   - `commit()` saves changes to the database file. Without it, changes are lost when the connection closes.

5. **"What's the difference between `fetchone()` and `fetchall()`?"**
   - `fetchone()` returns one row (or None). `fetchall()` returns a list of all matching rows.

---

## G. Module 17 Completion Checklist

| # | Syllabus Point | Status | Demonstrated |
|---|---------------|--------|-------------|
| 1 | CREATE | Done | `CREATE TABLE tasks` in init_db() |
| 2 | INSERT | Done | `INSERT INTO tasks` in create_task() |
| 3 | SELECT | Done | `SELECT * FROM` in all get_ functions |
| 4 | UPDATE | Done | `UPDATE tasks SET` in update_task() |
| 5 | DELETE | Done | `DELETE FROM tasks` in delete_task() |

**All 5 syllabus points for Module 17 are covered.**
