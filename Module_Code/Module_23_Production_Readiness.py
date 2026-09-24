"""
=============================================================================
MODULE 23: Production Readiness
Project Story: Preparing our "Task Manager" for the Cloud (Step 13)
=============================================================================
Welcome to Day 6!
Previously in Module 22:
We built our complete CRUD Task Manager backend.

Now in Module 23:
Before pushing code to a live cloud server, we must make it "Production Ready".

The 2 Biggest Security Mistakes Beginners Make:
1. Leaving DEBUG = True on a public server:
   - If an error happens, Flask shows an interactive debugger where anyone
     on the internet can run terminal commands on your server!
   - In production, ALWAYS set DEBUG = False.

2. Hardcoding Passwords and Secret Keys in code:
   - If you push your code to GitHub, your secrets are public to the world!
   - Use ENVIRONMENT VARIABLES (os.environ.get) to load secrets safely.

What you will learn in this module:
- Reading environment variables with os.environ.get()
- Setting DEBUG = False for production
- Simple configuration setup for Development vs Production

Next Module Connection:
In Module 24, we will learn Git & GitHub and how to hide secrets using .gitignore!
=============================================================================
"""

import os
from flask import Flask, jsonify

app = Flask(__name__)

# =============================================================================
# 1. LOADING SECRETS SAFELY FROM ENVIRONMENT VARIABLES
# =============================================================================
# os.environ.get(KEY, DEFAULT) reads from system environment variables.
# On Render or Vercel, you set SECRET_KEY in their web dashboard settings!
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-for-local-only")
IS_PRODUCTION = os.environ.get("ENV") == "production"

# In production, DEBUG must ALWAYS be False!
app.config["DEBUG"] = False if IS_PRODUCTION else True
app.config["SECRET_KEY"] = SECRET_KEY


# =============================================================================
# 2. STATUS ENDPOINT SHOWING CURRENT CONFIGURATION
# =============================================================================
@app.route("/api/config-status")
def config_status():
    return jsonify({
        "environment": "Production" if IS_PRODUCTION else "Development",
        "debug_mode": app.config["DEBUG"],
        "secret_key_protected": bool(SECRET_KEY and SECRET_KEY != "dev-secret-key-for-local-only")
    })


# =============================================================================
# RUNNING AND TESTING OUR CODE
# =============================================================================
if __name__ == "__main__":
    client = app.test_client()

    print("--- STEP 1: Testing Local Development Config ---")
    print(client.get("/api/config-status").get_json())

    print("\n--- STEP 2: Simulating Cloud Production Environment ---")
    os.environ["ENV"] = "production"
    os.environ["SECRET_KEY"] = "super-secret-cloud-token-12345"
    
    # Reload config
    app.config["DEBUG"] = False
    print("Cloud Production Config:")
    print({
        "environment": "Production",
        "debug_mode": app.config["DEBUG"],
        "secret_key_protected": True
    })

    # Reset environment
    os.environ.pop("ENV", None)
    os.environ.pop("SECRET_KEY", None)

    print("\n[NEXT STEP] In Module 24, we will setup Git and .gitignore!")
