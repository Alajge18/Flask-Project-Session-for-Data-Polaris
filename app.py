# ============================================================
# app.py — The Main Entry Point of TaskFlow (All Modules)
# ============================================================
# This is the MAIN file that creates and runs the Flask application.
#
# In the final version (Module 19+), this file is CLEAN because:
#   - Routes are in routes/task_routes.py and routes/user_routes.py
#   - Database operations are in database.py
#   - Forms are in forms.py
#   - Configuration is in config.py
#   - Data helpers are in models.py
#
# This file only does:
#   1. Create the Flask app
#   2. Load configuration
#   3. Initialize the database
#   4. Register blueprints
#   5. Set up error handlers
#   6. Run the server
#
# Modules Covered:
#   Module 10 — Flask Application creation
#   Module 19 — Project Architecture (blueprints)
#   Module 21 — Global error handlers
#   Module 23 — Production configuration
# ============================================================

from flask import Flask, jsonify
# Flask   → The framework itself, creates our web app
# jsonify → Converts Python dictionaries to JSON (for error handlers)

from config import Config
# Module 23 — Production Readiness: Load config from separate file
# Config class contains SECRET_KEY, DATABASE, DEBUG settings

from database import init_db
# Module 18 — Database initialization: creates tables on startup

from routes import task_bp, user_bp
# Module 19 — Project Architecture: Import blueprints
# task_bp → handles /tasks, /api/tasks routes
# user_bp → handles /api/users routes


# ============================================================
# CREATE THE FLASK APPLICATION
# ============================================================
# Module 10 — Introduction to Flask:
#   Flask(__name__) creates a new web application
#   __name__ tells Flask where this file is located
#   so it can find the templates/ and static/ folders
# ============================================================

app = Flask(__name__)

# --- Load Configuration ---
# Module 23 — Production Readiness:
#   from_object() reads all UPPERCASE attributes from the Config class
#   SECRET_KEY, DATABASE, DEBUG are loaded automatically
app.config.from_object(Config)


# --- Initialize the Database ---
# Module 18 — SQLite Integration:
#   init_db() creates the users and tasks tables if they don't exist
#   app_context() is needed because database operations require Flask to be "active"
with app.app_context():
    init_db()


# ============================================================
# REGISTER BLUEPRINTS
# ============================================================
# Module 19 — Project Architecture:
#   Blueprints organize routes into separate files.
#   register_blueprint() connects them to the main app.
#
#   After registration:
#     task_bp routes → /tasks, /api/tasks, etc.
#     user_bp routes → /api/users, etc.
# ============================================================

app.register_blueprint(task_bp)
# Task routes: /, /about, /tasks, /tasks/<id>, /tasks/add, /api/tasks, etc.

app.register_blueprint(user_bp)
# User routes: /api/users, /api/users/<id>


# ============================================================
# GLOBAL ERROR HANDLERS (Module 21)
# ============================================================
# These catch errors that happen ANYWHERE in the application.
# They return friendly JSON/HTML responses instead of ugly errors.
#
# Module 21 — Validation & Error Handling
# Module 9  — HTTP Status Codes
# ============================================================

@app.errorhandler(404)
def not_found(error):
    """
    Handle 404 Not Found errors.

    Module 9: 404 means the requested URL doesn't exist.
    This runs when someone visits a URL that has no route.
    """
    return jsonify({"error": "The requested resource was not found"}), 404


@app.errorhandler(500)
def server_error(error):
    """
    Handle 500 Internal Server errors.

    Module 9: 500 means something went wrong on the server.
    Module 23: In production, NEVER show detailed error info.
    """
    return jsonify({"error": "Something went wrong on our end"}), 500


# ============================================================
# RUN THE SERVER
# ============================================================
# Module 10 — Running a Flask Server:
#   This block runs ONLY when you execute: python app.py
#   It does NOT run when another file imports app.py
#   (e.g., gunicorn imports app.py in production)
#
# Module 1 — Variable Scope:
#   __name__ == "__main__" is True when you run: python app.py
#   __name__ == "app" when another file imports this module
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)
    # Module 10 — Debug Mode:
    #   debug=True gives us:
    #     1. Auto-reload: server restarts when you save code changes
    #     2. Error pages: shows detailed errors in the browser
    #   WARNING: Never use debug=True on a public server (Module 23)
    #
    # In production (Render), gunicorn runs the app:
    #   gunicorn app:app  (from the Procfile)
    #   Debug is controlled by config.py