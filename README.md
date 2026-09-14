# TaskFlow — Personal Task Management System

A beginner-friendly Flask project covering Modules 10–19.

## Features

- **View** all your tasks with status filter (Pending / In Progress / Completed)
- **Add** new tasks with title, description, and status
- **Edit** existing tasks
- **Delete** tasks
- **Dashboard** with task count stats

## Setup

```powershell
cd TaskFlow
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## Project Structure

```
TaskFlow/
├── app.py            — Flask app, all routes (HTML + API)
├── database.py       — SQLite connection and queries
├── models.py         — Data conversion helpers
├── forms.py          — Flask-WTF form classes
├── requirements.txt  — Python dependencies
├── tasks.db          — SQLite database (auto-created)
├── templates/        — HTML pages
│   ├── base.html
│   ├── index.html
│   ├── tasks.html
│   ├── add_task.html
│   ├── task_detail.html
│   └── edit_task.html
└── static/
    └── style.css     — Styling
```

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| POST   | /api/tasks | Create task |
| GET    | /api/tasks | List tasks |
| GET    | /api/tasks?status=pending | Filter tasks |
| GET    | /api/tasks/1 | Get task by ID |
| PUT    | /api/tasks/1 | Update task |
| DELETE | /api/tasks/1 | Delete task |
