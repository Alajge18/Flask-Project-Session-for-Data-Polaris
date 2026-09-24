# ============================================================
# config.py — Application Configuration (Module 23)
# ============================================================
# This file stores all configuration settings for the app.
#
# Why a separate config file?
#   - Keeps secrets OUT of app.py
#   - Easy to switch between development and production
#   - Environment variables for sensitive data
#
# Module 23 — Production Readiness:
#   - SECRET_KEY from environment variable
#   - DEBUG mode control
#   - Database path configuration
# ============================================================

import os
# os module lets us read ENVIRONMENT VARIABLES
# Environment variables are set OUTSIDE the code:
#   Windows: set SECRET_KEY=my-secret
#   Mac/Linux: export SECRET_KEY=my-secret
#   Render: Set in the dashboard → Environment section


class Config:
    """
    Application configuration class.

    Module 3 — OOP: Configuration as a class
    Module 23 — Production Readiness: environment variables

    Usage in app.py:
        from config import Config
        app.config.from_object(Config)
    """

    # --- Secret Key ---
    # Required for: CSRF protection (Flask-WTF), session data, flash messages
    # os.environ.get() reads from environment variables
    # The second argument is the DEFAULT (used in development)
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    # In production (Render):
    #   Set SECRET_KEY in Render dashboard → Environment Variables
    #   Use a long random string: python -c "import secrets; print(secrets.token_hex(32))"

    # --- Database Path ---
    DATABASE = os.environ.get("DATABASE", "tasks.db")
    # Default: tasks.db in the project folder
    # Can be overridden with environment variable if needed

    # --- Debug Mode ---
    # Development: True (auto-reload, detailed errors)
    # Production: False (generic errors, no auto-reload)
    DEBUG = os.environ.get("FLASK_DEBUG", "False").lower() in ("true", "1", "yes")
