# Module 16 — Database Fundamentals

---

## Module 16 Syllabus Checklist

| # | Topic | Status |
|---|-------|--------|
| 1 | Database | Covered below |
| 2 | Table | Covered below |
| 3 | Row | Covered below |
| 4 | Column | Covered below |
| 5 | Primary key | Covered below |
| 6 | Foreign key | Covered below |
| 7 | Relationships | Covered below |

---

## A. Concept Explanation — What is a Database?

### The Filing Cabinet Analogy

Imagine a filing cabinet in an office:
- The **cabinet** = the database (`tasks.db`)
- Each **drawer** = a table (`users`, `tasks`)
- Each **folder** in a drawer = a row (one user, one task)
- The **labels** on each folder = columns (name, email, status)

A database stores data **permanently**. Even when you turn off your computer, the data stays in the database file.

---

## B. Key Terms

| Term | What it is | TaskFlow example |
|------|-----------|-----------------|
| **Database** | A file that stores all your data | `tasks.db` |
| **Table** | A collection of related data (like a spreadsheet) | `users` table, `tasks` table |
| **Row** | One record in a table | User "Alice" is one row |
| **Column** | One piece of information | `name`, `email`, `status` |
| **Primary Key** | Unique ID for each row | `id` column (1, 2, 3...) |
| **Foreign Key** | A column that points to another table's row | `user_id` in tasks points to `id` in users |

---

## C. TaskFlow Database Schema

### Users Table

```
+----+-------+-------------------+
| id | name  | email             |
+----+-------+-------------------+
| 1  | Alice | alice@example.com |
| 2  | Bob   | bob@example.com   |
+----+-------+-------------------+
```

| Column | Type | Rules |
|--------|------|-------|
| `id` | INTEGER | Primary Key, Auto-increment |
| `name` | TEXT | NOT NULL (required) |
| `email` | TEXT | NOT NULL (required) |

### Tasks Table

```
+----+-------------+------------------+-----------+---------+
| id | title       | description      | status    | user_id |
+----+-------------+------------------+-----------+---------+
| 1  | Learn Flask | Understand routes| pending   | 1       |
| 2  | Build App   | Complete project | in_progress| 1      |
| 3  | Study SQL   | Database queries | completed | 2       |
+----+-------------+------------------+-----------+---------+
```

| Column | Type | Rules |
|--------|------|-------|
| `id` | INTEGER | Primary Key, Auto-increment |
| `title` | TEXT | NOT NULL (required) |
| `description` | TEXT | Optional |
| `status` | TEXT | NOT NULL, Default: 'pending' |
| `user_id` | INTEGER | NOT NULL, Foreign Key → users.id |

---

## D. Primary Key

A **primary key** uniquely identifies each row in a table. No two rows can have the same primary key.

```
Users table:
  id=1 → Alice (unique)
  id=2 → Bob (unique)
  id=1 → ???  ← IMPOSSIBLE! Can't have two id=1
```

In TaskFlow:
```sql
id INTEGER PRIMARY KEY AUTOINCREMENT
```
- `PRIMARY KEY` → This column is the unique identifier
- `AUTOINCREMENT` → SQLite automatically assigns the next number (1, 2, 3...)

---

## E. Foreign Key — Connecting Tables

A **foreign key** is a column in one table that **points to** a row in another table.

```
USERS TABLE                    TASKS TABLE
+----+-------+                 +----+-------------+---------+
| id | name  |                 | id | title       | user_id |
+----+-------+                 +----+-------------+---------+
| 1  | Alice | ←───────────── | 1  | Learn Flask | 1       |
| 2  | Bob   | ←──────┐       | 2  | Build App   | 1       |
+----+-------+        └────── | 3  | Study SQL   | 2       |
                               +----+-------------+---------+
```

- Task 1 (`Learn Flask`) has `user_id = 1` → belongs to Alice
- Task 2 (`Build App`) has `user_id = 1` → also belongs to Alice
- Task 3 (`Study SQL`) has `user_id = 2` → belongs to Bob

In SQL:
```sql
FOREIGN KEY (user_id) REFERENCES users (id)
```

This means: `user_id` in the tasks table MUST match an existing `id` in the users table.

---

## F. One-to-Many Relationship

```
ONE user → MANY tasks
Alice (id=1) → Task 1 (Learn Flask), Task 2 (Build App)
Bob (id=2) → Task 3 (Study SQL)

ONE task → ONE user
Task 1 → Alice (user_id=1)
Task 3 → Bob (user_id=2)
```

This is called a **one-to-many relationship**:
- One user can have many tasks
- Each task belongs to exactly one user

---

## G. Common Mistakes and Fixes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Creating a task with `user_id=99` (doesn't exist) | Foreign key violation | Check if user exists before creating task |
| Forgetting `PRAGMA foreign_keys = ON` | SQLite doesn't enforce foreign keys | Add this line in `get_db()` |
| Confusing primary key with foreign key | They're different! | Primary key = unique ID for THIS table. Foreign key = points to ANOTHER table |
| No primary key on a table | Can't uniquely identify rows | Always add `id INTEGER PRIMARY KEY` |

---

## H. Practice Task

1. Look at the tasks.db file using an SQLite viewer or the sqlite3 command line.
2. Try to understand which user owns which tasks by looking at `user_id`.
3. Draw the relationship between users and tasks on paper.

---

## I. Teaching Questions

1. **"What is a primary key?"**
   - A unique ID for each row. No two rows can have the same primary key.

2. **"What is a foreign key?"**
   - A column that points to a primary key in another table. Links tables together.

3. **"Can a user have zero tasks?"**
   - Yes! A user exists independently. Tasks are optional.

4. **"Can a task exist without a user?"**
   - No! `user_id` is NOT NULL and must reference an existing user.

5. **"What's the difference between a table and a database?"**
   - A database (tasks.db) contains multiple tables (users, tasks).

---

## J. Module 16 Completion Checklist

| # | Syllabus Point | Status | Demonstrated |
|---|---------------|--------|-------------|
| 1 | Database | Done | `tasks.db` file explained |
| 2 | Table | Done | `users` and `tasks` tables |
| 3 | Row | Done | Each user/task is a row |
| 4 | Column | Done | id, name, email, title, status, user_id |
| 5 | Primary key | Done | `id INTEGER PRIMARY KEY AUTOINCREMENT` |
| 6 | Foreign key | Done | `FOREIGN KEY (user_id) REFERENCES users (id)` |
| 7 | Relationships | Done | One-to-many: one user → many tasks |

**All 7 syllabus points for Module 16 are covered.**
