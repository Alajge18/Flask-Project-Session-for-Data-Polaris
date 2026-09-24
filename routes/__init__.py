# ============================================================
# routes/__init__.py — Blueprint Package Initialization (Module 19)
# ============================================================
# This file makes the routes/ folder a Python PACKAGE.
# A package is a folder that contains Python modules.
#
# Module 2  — Modules and Packages: __init__.py creates a package
# Module 19 — Project Architecture: separating routes into files
# ============================================================

# This file can be empty — its existence is what makes
# routes/ a package. But we import our blueprints here
# for convenient access.

from routes.task_routes import task_bp
from routes.user_routes import user_bp
# Now app.py can do:
#   from routes import task_bp, user_bp
