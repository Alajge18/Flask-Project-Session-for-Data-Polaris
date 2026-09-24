# ============================================================
# routes/user_routes.py — User Route Blueprint (Module 19, 20, 21)
# ============================================================
# All user-related routes are here (API only — no HTML forms for users).
#
# Module 19 — Project Architecture: Blueprint for user routes
# Module 20 — API Endpoint Design: POST /users, GET /users/<id>
# Module 21 — Validation & Error Handling
# ============================================================

from flask import Blueprint, request, jsonify

from database import create_user, get_user_by_id
# Import database functions for user operations

from models import user_to_dict
# Convert database rows to dictionaries for JSON responses


# --- Create the Blueprint ---
# Module 19 — Blueprints:
#   Separate user routes from task routes
user_bp = Blueprint("users", __name__)


# ============================================================
# USER API ROUTES
# ============================================================
# Users are managed via API only (no HTML forms in this version).
# This keeps the workshop focused on task management.
#
# Module 20 — API Endpoint Design:
#   POST /api/users       → Create a new user
#   GET  /api/users/<id>  → Get user by ID
# ============================================================


# --- API: Create a User ---
# Module 8  — HTTP Methods: POST = Create
# Module 9  — Status Codes: 201 Created, 400 Bad Request
# Module 21 — Validation
@user_bp.route("/api/users", methods=["POST"])
def api_create_user():
    """
    Create a new user via JSON.

    Module 15 — APIs:
      Expected JSON body:
        {"name": "Alice", "email": "alice@email.com"}

    Module 21 — Validation:
      - Name is required
      - Email is required
    """
    data = request.get_json()

    # Module 21 — Validation: Check required fields
    if not data:
        return jsonify({"error": "Request body is required."}), 400

    if not data.get("name") or not data.get("name", "").strip():
        return jsonify({"error": "Name is required."}), 400

    if not data.get("email") or not data.get("email", "").strip():
        return jsonify({"error": "Email is required."}), 400

    # Module 6 — Exception Handling: database might raise error (duplicate email)
    try:
        user_id = create_user(data["name"].strip(), data["email"].strip())
        user = get_user_by_id(user_id)

        return jsonify({
            "message": "User created successfully",
            "user": user_to_dict(user)
        }), 201
        # Module 9: 201 Created

    except Exception as e:
        # Module 6: Catch database errors (e.g., duplicate email)
        return jsonify({"error": f"Could not create user: {str(e)}"}), 400


# --- API: Get a User ---
# Module 8  — HTTP Methods: GET = Read
# Module 11 — Dynamic Route: <int:user_id>
@user_bp.route("/api/users/<int:user_id>", methods=["GET"])
def api_get_user(user_id):
    """
    Get a user by ID.

    Module 11 — Dynamic Routes:
      <int:user_id> extracts the ID from the URL
      /api/users/1 → user_id=1
    """
    user = get_user_by_id(user_id)

    if not user:
        return jsonify({"error": "User not found."}), 404
        # Module 9: 404 Not Found

    return jsonify(user_to_dict(user)), 200
