"""
=============================================================================
MODULE 10: Introduction to Flask
Topic: Your Very First Flask App (Foundation Phase Finale)
=============================================================================
Welcome to Day 2!
In this module, we introduce the Flask web framework conceptually:
what it is, how it handles incoming web requests, and how to write
a "Hello World" application.

What you will learn in this module:
1. What Flask is (a lightweight Python web micro-framework)
2. Creating the WSGI app: app = Flask(__name__)
3. Defining simple routes: @app.route('/') and @app.route('/about')
4. Returning HTML text to a browser
5. Understanding Debug Mode (debug=True)

=============================================================================
PROJECT ANNOUNCEMENT:
In the next module (Module 11), we officially begin our hands-on project:
THE TASK MANAGER APPLICATION (TaskFlow)!
Everything from Module 11 through Module 26 will build, structure, persist,
and deploy this complete project step-by-step.
=============================================================================
"""

from flask import Flask

# 1. Initialize the Flask application instance
app = Flask(__name__)


# =============================================================================
# 2. DEFINING INTRODUCTORY WEB ROUTES
# =============================================================================

@app.route("/")
def home():
    """
    When a user opens http://127.0.0.1:5000/ in their browser,
    Flask runs this function and returns the HTML text.
    """
    return "<h1>Hello, World!</h1><p>Welcome to Flask Web Development.</p>"


@app.route("/about")
def about():
    """
    When a user visits http://127.0.0.1:5000/about
    """
    return "<h2>About This Course</h2><p>Learning Python Backend and Flask from the ground up.</p>"


# =============================================================================
# RUNNING OUR FLASK APP
# =============================================================================
if __name__ == "__main__":
    print("--- Testing Introductory Flask Routes ---")

    # Automated test of routes
    client = app.test_client()
    print("GET /      :", client.get("/").data.decode("utf-8").strip())
    print("GET /about :", client.get("/about").data.decode("utf-8").strip())

    print("\n" + "=" * 65)
    print("FOUNDATION PHASE COMPLETE!")
    print("Hands-on Project Implementation starts next in MODULE 11: Task Manager!")
    print("=" * 65)

    # To run as a live web server on your browser, uncomment below:
    # app.run(debug=True, port=5000)
