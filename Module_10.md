# Module 10 — Introduction to Flask

---

## Module 10 Syllabus Checklist

| # | Topic | Status |
|---|-------|--------|
| 1 | What Flask is | Covered below |
| 2 | Why Flask is used | Covered below |
| 3 | Flask vs Django vs FastAPI | Covered below |
| 4 | Flask installation | Covered below |
| 5 | Virtual environments | Covered below |
| 6 | requirements.txt | Covered below |
| 7 | Creating a Flask application | Covered below |
| 8 | Running a Flask server | Covered below |
| 9 | Debug mode | Covered below |
| 10 | First Flask application | Covered below |
| 11 | Basic Flask routes | Covered below |

---

## A. Concept Explanation — What is Flask?

### What is a Web Framework?

Imagine you want to build a house. You **could** mix cement, cut wood, shape bricks — all by hand. Or you could use **pre-made building blocks** that let you focus on **designing** the house instead of manufacturing raw materials.

A **web framework** is a collection of pre-made building blocks for creating websites. Instead of writing low-level networking code yourself, a framework handles that for you.

### What is Flask?

**Flask** is a Python web framework. It lets you build web applications using Python.

Flask is called a **"micro-framework"** because:
- It gives you the **essentials** — routing, request handling, response sending, template rendering.
- It does **not** force you to use a specific database or project structure.
- You pick and choose what you need.

> **Analogy**: Flask is like a basic kitchen with a stove, sink, and counter. You bring your own pots and ingredients. Django is like a fully equipped restaurant kitchen — everything is there, but you must follow its setup.

### Key Flask Facts
- Created by **Armin Ronacher** in 2010.
- Written in **Python**.
- Used by **Netflix, Reddit, Airbnb, LinkedIn**.
- Free and open source.

---

## B. Flask vs Django vs FastAPI

| Feature | Flask | Django | FastAPI |
|---------|-------|--------|---------|
| **Type** | Micro-framework | Full-stack framework | Modern API framework |
| **Learning curve** | Easy | Moderate | Moderate |
| **Built-in features** | Minimal | Many (admin, ORM, auth) | API-focused (auto docs) |
| **Database** | Your choice | Built-in ORM | Your choice |
| **Best for** | Small-medium apps, learning | Large apps, CMS | High-performance APIs |
| **Template engine** | Jinja2 | Django Templates | Not included |
| **Flexibility** | Very high | Moderate | High |

**Why Flask for learning?**
1. Simplest to learn.
2. You build everything yourself, so you understand every concept.
3. It doesn't hide complexity.

---

## C. Virtual Environments

### What is a Virtual Environment?

A **virtual environment** is an isolated Python workspace. Each project gets its own set of installed packages.

> **Analogy**: Your computer is an apartment building. Each apartment (virtual environment) has its own furniture (packages). Installing something in Apartment A doesn't affect Apartment B.

### Why Do We Need It?

Without virtual environments, Project A (needs Flask 2.0) and Project B (needs Flask 3.0) would conflict. With virtual environments, each project has its own Flask version.

### Setup Commands (Windows PowerShell)

```powershell
# Step 1: Navigate to the project
cd "c:\Users\chaud\Desktop\Projects\Data polaris\task management system by me\TaskFlow"

# Step 2: Create virtual environment
python -m venv venv

# Step 3: Activate it (you'll see "(venv)" in your prompt)
.\venv\Scripts\Activate

# Step 4: Install packages
pip install -r requirements.txt

# Step 5: Verify installation
pip list
```

> **Common Error**: If you get an execution policy error:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

---

## D. requirements.txt

A text file listing every package your project needs:

```text
Flask==3.1.1
Flask-WTF==1.2.2
WTForms==3.2.1
```

- `Flask==3.1.1` → Install Flask version 3.1.1 exactly.
- Anyone can run `pip install -r requirements.txt` to get the same setup.

---

## E. Code Implementation — First Flask App

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to TaskFlow — Your Task Management System!"

if __name__ == "__main__":
    app.run(debug=True)
```

### Line-by-Line Explanation

| Line | What it does | Why |
|------|-------------|-----|
| `from flask import Flask` | Imports the Flask class | Need it to create a web app |
| `app = Flask(__name__)` | Creates a Flask application | `__name__` tells Flask where to find files |
| `@app.route("/")` | Decorator: maps URL `/` to the function below | When user visits `/`, run `home()` |
| `def home():` | View function — decides what user sees | Called automatically by Flask |
| `return "Welcome..."` | Sends text to the browser | This becomes the HTTP response |
| `if __name__ == "__main__":` | Only runs when file is executed directly | Prevents running during imports |
| `app.run(debug=True)` | Starts the Flask development server | `debug=True` enables auto-reload + error pages |

### What is `__name__`?

When you run `python app.py`, Python sets `__name__` to `"__main__"`. Flask uses this to find your project's location (where templates/ and static/ are).

### What is `@app.route("/")`?

A **decorator** — a special tag above a function that modifies its behavior. `@app.route("/")` tells Flask: "When someone visits `/`, run the function below."

### What is Debug Mode?

`debug=True` enables:
1. **Auto-reload**: Flask restarts when you save code changes.
2. **Error pages**: Shows detailed errors in the browser.

> **WARNING**: NEVER use `debug=True` on a public server. The debugger lets anyone execute Python code on your machine.

---

## F. Execution Flow

What happens when you visit `http://127.0.0.1:5000/`:

```
Step 1: You type the URL → Browser sends GET / HTTP/1.1
Step 2: Flask server receives the request
Step 3: Flask matches "/" to @app.route("/") → home()
Step 4: home() returns "Welcome to TaskFlow..."
Step 5: Flask sends HTTP 200 OK + the text back
Step 6: Browser displays the text
```

### What is 127.0.0.1?
- **localhost** — means "this computer."
- `:5000` is the port number (like a door number). Flask uses port 5000 by default.

---

## G. Running the Application

```powershell
# Make sure venv is active
.\venv\Scripts\Activate

# Run the server
python app.py

# You should see:
#  * Running on http://127.0.0.1:5000
#  * Debug mode: on

# Open browser → http://127.0.0.1:5000/

# Stop the server
# Press Ctrl+C in the terminal
```

---

## H. Common Mistakes and Fixes

| Mistake | Error | Fix |
|---------|-------|-----|
| Running without venv active | `ModuleNotFoundError: No module named 'flask'` | Activate venv: `.\venv\Scripts\Activate` |
| Port already in use | `OSError: Address already in use` | Use different port: `app.run(port=5001)` |
| Using backslash in route | `@app.route("\")` | Use forward slash: `@app.route("/")` |
| Using `print()` instead of `return` | Page shows nothing | `return` sends to browser, `print` goes to terminal |
| Missing `if __name__` guard | Server starts on import | Always wrap `app.run()` in the if block |

---

## I. Practice Task

1. Add a route `/about` that returns: `"TaskFlow v1.0 — Built with Flask"`
2. Add a route `/contact` that returns: `"Contact: taskflow@example.com"`
3. Run the server and visit both URLs in your browser.
4. Visit a URL that doesn't exist (like `/xyz`) and observe the 404 error.

---

## J. Teaching Questions

1. **"What does `Flask(__name__)` do?"**
   - Creates a Flask app. `__name__` tells Flask where to find templates and static files.

2. **"What does `@app.route("/")` do?"**
   - A decorator that maps the URL `/` to the function below it.

3. **"Difference between `print("Hello")` and `return "Hello"` in a route?"**
   - `print` goes to the terminal. `return` goes to the user's browser.

4. **"Why not use `debug=True` on a public server?"**
   - The debugger lets anyone run Python code on your server — security risk.

5. **"What happens if you visit a URL with no route?"**
   - Flask returns a 404 Not Found error.

---

## K. Module 10 Completion Checklist

| # | Syllabus Point | Status | Demonstrated |
|---|---------------|--------|-------------|
| 1 | What Flask is | Done | Concept explanation |
| 2 | Why Flask is used | Done | Comparison + reasons |
| 3 | Flask vs Django vs FastAPI | Done | Comparison table |
| 4 | Flask installation | Done | `pip install -r requirements.txt` |
| 5 | Virtual environments | Done | `python -m venv venv` |
| 6 | requirements.txt | Done | Created and explained |
| 7 | Creating a Flask application | Done | `app = Flask(__name__)` |
| 8 | Running a Flask server | Done | `python app.py` |
| 9 | Debug mode | Done | `app.run(debug=True)` |
| 10 | First Flask application | Done | Working welcome page |
| 11 | Basic Flask routes | Done | `@app.route("/")` |

**All 11 syllabus points for Module 10 are covered.**
