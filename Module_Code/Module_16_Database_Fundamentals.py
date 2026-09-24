"""
=============================================================================
MODULE 16: Database Fundamentals
Project Story: Building our "Task Manager" Database (Step 6)
=============================================================================
Welcome to Day 4!
Previously in Module 15:
We noticed a huge problem: every time the Flask server stops, ALL TASKS DISAPPEAR!
That's because variables only exist in computer RAM (in-memory).

Now in Module 16:
We introduce Databases to store our tasks PERMANENTLY on disk.

What you will learn in this module:
1. Tables: A grid where our task records live
2. Columns: Specific fields (id, title, status)
3. Rows: A single task record
4. Primary Key (PK): A unique number automatically assigned to each task
5. Creating our first SQLite database table in Python

Next Module Connection:
In Module 17, we will learn the 4 essential SQL commands (INSERT, SELECT,
UPDATE, DELETE) to manipulate this table!
=============================================================================
"""

import sqlite3

# =============================================================================
# 1. CONNECTING TO A DATABASE
# =============================================================================
# sqlite3 is built directly into Python! No installation required.
# ":memory:" creates a temporary database for testing, but in real life
# we use a file like "tasks.db".
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

# =============================================================================
# 2. DESIGNING AND CREATING OUR TASKS TABLE
# =============================================================================
# CREATE TABLE statement defines the structure of our data:
cursor.execute("""
    CREATE TABLE tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        status TEXT DEFAULT 'Pending'
    );
""")
conn.commit()

# =============================================================================
# 3. INSERTING INITIAL SAMPLE DATA
# =============================================================================
cursor.execute("INSERT INTO tasks (title, status) VALUES ('Learn Database Concepts', 'Completed');")
cursor.execute("INSERT INTO tasks (title, status) VALUES ('Write First SQL Query', 'Pending');")
conn.commit()

# =============================================================================
# RUNNING AND TESTING OUR CODE
# =============================================================================
if __name__ == "__main__":
    print("--- STEP 1: Inspecting Table Structure ---")
    print("Created 'tasks' table with columns: (id, title, status)")

    print("\n--- STEP 2: Reading Rows from our Database Table ---")
    cursor.execute("SELECT id, title, status FROM tasks;")
    rows = cursor.fetchall()
    
    for row in rows:
        print(f"  Row -> ID: {row[0]}, Title: '{row[1]}', Status: '{row[2]}'")

    conn.close()
    print("\n[NEXT STEP] In Module 17, we will learn raw SQL commands to CRUD tasks!")
