"""
=============================================================================
MODULE 17: SQL Basics (CRUD Operations)
Project Story: Building our "Task Manager" Database (Step 7)
=============================================================================
Previously in Module 16:
We created our tasks table in SQLite.

Now in Module 17:
We learn how to communicate with the database using SQL (Structured Query Language).
Every backend developer must know the 4 foundational commands (CRUD):

1. CREATE : INSERT INTO tasks (title, status) VALUES (?, ?)
2. READ   : SELECT id, title, status FROM tasks
3. UPDATE : UPDATE tasks SET status = ? WHERE id = ?
4. DELETE : DELETE FROM tasks WHERE id = ?

CRITICAL SECURITY RULE FOR BEGINNERS:
Always use the '?' placeholder! Never use string concatenation (like f"{title}"),
as that makes your app vulnerable to hackers (SQL Injection).

Next Module Connection:
In Module 18, we will connect SQLite directly to Flask so our web routes
save tasks into a real database file!
=============================================================================
"""

import sqlite3

# Connect to in-memory database and enable dictionary-style rows
conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Setup tasks table
cursor.execute("""
    CREATE TABLE tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        status TEXT DEFAULT 'Pending'
    );
""")
conn.commit()


# =============================================================================
# 1. INSERT (Create)
# =============================================================================
def add_task(title, status="Pending"):
    # Using '?' placeholders protects against SQL injection!
    cursor.execute("INSERT INTO tasks (title, status) VALUES (?, ?);", (title, status))
    conn.commit()
    return cursor.lastrowid


# =============================================================================
# 2. SELECT (Read)
# =============================================================================
def get_all_tasks():
    cursor.execute("SELECT id, title, status FROM tasks ORDER BY id ASC;")
    return cursor.fetchall()


# =============================================================================
# 3. UPDATE (Update)
# =============================================================================
def complete_task(task_id):
    cursor.execute("UPDATE tasks SET status = 'Completed' WHERE id = ?;", (task_id,))
    conn.commit()


# =============================================================================
# 4. DELETE (Delete)
# =============================================================================
def delete_task(task_id):
    cursor.execute("DELETE FROM tasks WHERE id = ?;", (task_id,))
    conn.commit()


# =============================================================================
# RUNNING AND TESTING OUR CODE
# =============================================================================
if __name__ == "__main__":
    print("--- STEP 1: Inserting Tasks with SQL INSERT ---")
    id1 = add_task("Learn SQL Syntax", status="Completed")
    id2 = add_task("Connect SQLite to Flask", status="Pending")
    id3 = add_task("Delete this test task", status="Pending")
    print(f"Added tasks with IDs: {id1}, {id2}, {id3}")

    print("\n--- STEP 2: Querying Tasks with SQL SELECT ---")
    for row in get_all_tasks():
        print(f"  [Task #{row['id']}] {row['title']} -> {row['status']}")

    print("\n--- STEP 3: Updating Task #2 with SQL UPDATE ---")
    complete_task(id2)
    print("Task #2 is now marked as Completed!")

    print("\n--- STEP 4: Deleting Task #3 with SQL DELETE ---")
    delete_task(id3)
    print("Task #3 deleted. Remaining tasks:")
    for row in get_all_tasks():
        print(f"  [Task #{row['id']}] {row['title']} -> {row['status']}")

    conn.close()
    print("\n[NEXT STEP] In Module 18, we will connect this SQLite code to Flask!")
