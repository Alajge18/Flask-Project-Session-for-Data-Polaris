# TaskFlow — Task Management System

A complete Flask + SQLite backend built step-by-step across 26 modules (6-day workshop).

## Features

- ✓ **Create** tasks with title and description
- ✓ **View** all tasks with status filter (Pending / In Progress / Completed)
- ✓ **Edit** existing tasks
- ✓ **Delete** tasks
- ✓ **Search** tasks by title or description
- ✓ **Dashboard** with task count statistics
- ✓ **REST API** with JSON endpoints
- ✓ **User management** via API
- ✓ **Form validation** with Flask-WTF and CSRF protection
- ✓ **Error handling** with proper HTTP status codes
- ✓ **SQLite database** for persistent storage

## Setup

```powershell
# Clone the repository
git clone https://github.com/YOUR_USERNAME/task-management.git
cd task-management

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## Project Structure

```
task-management/
├── app.py                 — Main Flask app (blueprint registration)
├── config.py              — Configuration (env vars, secrets)
├── database.py            — SQLite connection and CRUD queries
├── models.py              — Data conversion helpers
├── forms.py               — Flask-WTF form classes
├── task_manager.py        — Day 1: Pure Python CLI Task Manager
├── requirements.txt       — Python dependencies
├── Procfile               — Render deployment command
├── vercel.json            — Vercel deployment config (optional)
├── tasks.db               — SQLite database (auto-created)
├── routes/
│   ├── __init__.py        — Blueprint imports
│   ├── task_routes.py     — Task routes (HTML + API)
│   └── user_routes.py     — User routes (API)
├── templates/
│   ├── base.html          — Parent template (nav, layout)
│   ├── index.html         — Homepage / dashboard
│   ├── about.html         — About page
│   ├── tasks.html         — Task list with filters
│   ├── add_task.html      — Add task form
│   ├── edit_task.html     — Edit task form
│   └── task_detail.html   — Single task details
└── static/
    └── style.css          — Styling
```

## API Endpoints

### Tasks

| Method | URL | Description |
|--------|-----|-------------|
| GET    | /api/tasks | List all tasks |
| GET    | /api/tasks?status=pending | Filter tasks by status |
| GET    | /api/tasks/1 | Get task by ID |
| POST   | /api/tasks | Create a new task |
| PUT    | /api/tasks/1 | Update a task |
| DELETE | /api/tasks/1 | Delete a task |

### Users

| Method | URL | Description |
|--------|-----|-------------|
| POST   | /api/users | Create a new user |
| GET    | /api/users/1 | Get user by ID |

## Technology Stack

| Category | Technology |
|----------|-----------|
| Language | Python |
| Framework | Flask |
| Database | SQLite |
| Forms | Flask-WTF / WTForms |
| Templates | Jinja2 |
| API Format | JSON |
| Deployment | Render / Vercel |

## Module Coverage (26 Modules)

| Day | Modules | Focus |
|-----|---------|-------|
| 1 | 1-6 | Python: Functions, OOP, Decorators, Exceptions |
| 2 | 7-10 | Backend Fundamentals, First Flask App |
| 3 | 11-15 | Routes, Jinja2 Forms, Flask-WTF, REST APIs |
| 4 | 16-18 | Database Fundamentals, SQL, SQLite |
| 5 | 19-22 | Project Architecture, CRUD, Validation |
| 6 | 23-26 | Production, Git, Render, Vercel |

## Deployment

### Render (Primary)

1. Push code to GitHub
2. Create a new Web Service on [render.com](https://render.com)
3. Connect your GitHub repo
4. Set Build Command: `pip install -r requirements.txt`
5. Set Start Command: `gunicorn app:app`
6. Add environment variable: `SECRET_KEY`

### Vercel (Optional)

1. Install Vercel CLI: `npm i -g vercel`
2. Run: `vercel`
3. Follow prompts
