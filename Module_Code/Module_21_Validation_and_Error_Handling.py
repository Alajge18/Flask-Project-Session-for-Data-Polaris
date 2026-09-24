"""
=============================================================================
MODULE 21: Validation and Error Handling
Project Story: Building our "Task Manager" API (Step 11)
=============================================================================
Previously in Module 20:
We designed clean REST API endpoints.

Now in Module 21:
What happens if a client passes empty data or visits a URL that doesn't exist?
By default, Flask returns an HTML error page. But REST API clients (like mobile apps)
expect JSON even when an error happens!

What you will learn in this module:
1. Input validation: checking required fields and data length
2. Returning 400 Bad Request when validation fails
3. Custom @app.errorhandler(404) to return JSON instead of HTML
4. Graceful error messages that guide the API user

Next Module Connection:
In Module 22, we will combine all of Days 1-5 into the COMPLETE CRUD BACKEND!
=============================================================================
"""

from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = []

# =============================================================================
# 1. CENTRALIZED 404 ERROR HANDLER (Always return JSON!)
# =============================================================================
@app.errorhandler(404)
def not_found_error(error):
    """Overrides Flask's default HTML 404 page with clean JSON."""
    return jsonify({
        "success": False,
        "error": "The requested API endpoint or task does not exist."
    }), 404


# =============================================================================
# 2. ENDPOINT WITH INPUT VALIDATION
# =============================================================================
@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json()

    # Rule 1: Must be valid JSON
    if not data:
        return jsonify({"success": False, "error": "Request body must be JSON."}), 400

    # Rule 2: Title must be present and not just spaces
    title = data.get("title", "").strip()
    if not title:
        return jsonify({"success": False, "error": "Field 'title' is required."}), 400

    # Rule 3: Title must be at least 3 characters
    if len(title) < 3:
        return jsonify({"success": False, "error": "Title must be at least 3 characters."}), 400

    # Rule 4: Status must be valid if provided
    status = data.get("status", "Pending")
    if status not in ["Pending", "In Progress", "Completed"]:
        return jsonify({"success": False, "error": "Status must be Pending, In Progress, or Completed."}), 400

    # All validations passed!
    new_task = {"id": len(tasks) + 1, "title": title, "status": status}
    tasks.append(new_task)

    return jsonify({"success": True, "task": new_task}), 201


# =============================================================================
# RUNNING AND TESTING OUR CODE
# =============================================================================
if __name__ == "__main__":
    client = app.test_client()

    print("--- STEP 1: Testing Validation Failure (Empty Title) ---")
    r1 = client.post("/api/tasks", json={"title": "  "})
    print("Status:", r1.status_code)
    print("Response:", r1.get_json())

    print("\n--- STEP 2: Testing Validation Failure (Invalid Status) ---")
    r2 = client.post("/api/tasks", json={"title": "Do Homework", "status": "Finished"})
    print("Status:", r2.status_code)
    print("Response:", r2.get_json())

    print("\n--- STEP 3: Testing Valid Creation ---")
    r3 = client.post("/api/tasks", json={"title": "Build Complete CRUD App", "status": "In Progress"})
    print("Status:", r3.status_code)
    print("Response:", r3.get_json())

    print("\n--- STEP 4: Testing 404 JSON Handler ---")
    r4 = client.get("/api/unknown-route")
    print("Status:", r4.status_code)
    print("Response (Clean JSON):", r4.get_json())

    print("\n[NEXT STEP] In Module 22, we build the Complete CRUD Backend combining everything!")
