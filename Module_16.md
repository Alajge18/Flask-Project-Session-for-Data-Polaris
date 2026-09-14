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

---

## A. Concept Explanation — What is a Database?

### The Filing Cabinet Analogy

Imagine a filing cabinet in an office:
- The **cabinet** = the database (`tasks.db`)
- Each **drawer** = a table (`tasks`)
- Each **folder** in a drawer = a row (one task)
- The **labels** on each folder = columns (title, status, description)

A database stores data **permanently**. Even when you turn off your computer, the data stays in the database file.

---

## B. Key Terms

| Term | What it is | TaskFlow example |
|------|-----------|-----------------
| **Database** | A file that stores all your data | `tasks.db` |
| **Table** | A collection of related data (like a spreadsheet) | `tasks` table |
| **Row** | One record in a table | Task "Learn Flask" is one row |
| **Column** | One piece of information | `title`, `description`, `status` |
| **Primary Key** | Unique ID for each row | `id` column (1, 2, 3...) |

---

## C. TaskFlow Database Schema

### Tasks Table

```
+----+-------------+------------------+-----------+---------------------+
| id | title       | description      | status    | created_at          |
+----+-------------+------------------+-----------+---------------------+
| 1  | Learn Flask | Understand routes| pending   | 2026-09-14 15:30:00 |
| 2  | Build App   | Complete project | in_progress| 2026-09-14 16:00:00|
| 3  | Study SQL   | Database queries | completed | 2026-09-14 16:30:00 |
+----+-------------+------------------+-----------+---------------------+
```

| Column | Type | Rules |
|--------|------|-------|
| `id` | INTEGER | Primary Key, Auto-increment |
| `title` | TEXT | NOT NULL (required) |
| `description` | TEXT | Optional |
| `status` | TEXT | NOT NULL, Default: 'pending' |
| `created_at` | TIMESTAMP | Auto-filled by the database |

---

## D. Primary Key

A **primary key** uniquely identifies each row in a table. No two rows can have the same primary key.

```
Tasks table:
  id=1 → Learn Flask (unique)
  id=2 → Build App (unique)
  id=1 → ???  ← IMPOSSIBLE! Can't have two id=1
```

In TaskFlow:
```sql
id INTEGER PRIMARY KEY AUTOINCREMENT
```
- `PRIMARY KEY` → This column is the unique identifier
- `AUTOINCREMENT` → SQLite automatically assigns the next number (1, 2, 3...)

---

## E. Common Mistakes and Fixes

| Mistake | Problem | Fix |
|---------|---------|-----|
| No primary key on a table | Can't uniquely identify rows | Always add `id INTEGER PRIMARY KEY` |
| Forgetting NOT NULL | Empty values allowed in required fields | Add NOT NULL to required columns |
| Confusing table with database | They're different! | Database (tasks.db) contains tables (tasks) |

---

## F. Practice Task

1. Look at the tasks.db file using an SQLite viewer or the sqlite3 command line.
2. Try to understand the structure of the tasks table.
3. Draw the table schema on paper.

---

## G. Teaching Questions

1. **"What is a primary key?"**
   - A unique ID for each row. No two rows can have the same primary key.

2. **"What does AUTOINCREMENT do?"**
   - SQLite automatically assigns the next number (1, 2, 3...) for new rows.

3. **"Can a task have an empty title?"**
   - No! The `title` column has NOT NULL — it must have a value.

4. **"What's the difference between a table and a database?"**
   - A database (tasks.db) contains tables (tasks). A table is like a spreadsheet inside the database.

---

## H. Module 16 Completion Checklist

| # | Syllabus Point | Status | Demonstrated |
|---|---------------|--------|-------------|
| 1 | Database | Done | `tasks.db` file explained |
| 2 | Table | Done | `tasks` table |
| 3 | Row | Done | Each task is a row |
| 4 | Column | Done | id, title, description, status, created_at |
| 5 | Primary key | Done | `id INTEGER PRIMARY KEY AUTOINCREMENT` |

**All 5 syllabus points for Module 16 are covered.**
