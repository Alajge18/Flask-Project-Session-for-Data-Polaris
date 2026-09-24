"""
=============================================================================
MODULE 26: Serverless Deployment with Vercel
Project Story: Exploring Serverless Architecture (Step 16 — Final Capstone)
=============================================================================
Previously in Module 25:
We deployed to Render where our server stays running 24/7.

Now in Module 26:
We explore SERVERLESS deployment on Vercel!

What is Serverless?
In serverless hosting:
- There is NO server running continuously.
- When a user visits your URL, Vercel starts your Flask code in milliseconds,
  processes the request, sends back the answer, and goes to sleep!
- It is ultra-fast, scales automatically to millions of requests, and is free
  for small personal projects.

What is vercel.json?
A configuration file placed in the root directory that tells Vercel how to route
incoming web requests to your Flask application.

What you will learn in this module:
1. The difference between Traditional servers (Render) and Serverless (Vercel)
2. The structure of vercel.json
3. Why serverless apps connect to external databases (like PostgreSQL/Supabase)
=============================================================================
"""

import json

# =============================================================================
# 1. THE vercel.json CONFIGURATION
# =============================================================================
VERCEL_CONFIG = {
    "builds": [
        {
            "src": "app.py",
            "use": "@vercel/python"
        }
    ],
    "routes": [
        {
            "src": "/(.*)",
            "dest": "app.py"
        }
    ]
}

VERCEL_STEPS = """
---------------------------------------------------------------------
HOW TO DEPLOY ON VERCEL (EASY):
---------------------------------------------------------------------
1. Ensure 'vercel.json' is in your repository root.
2. Go to https://vercel.com/new and sign in with GitHub.
3. Select your repository and click "Deploy"!
4. Vercel automatically gives you a lightning-fast global URL:
   https://my-task-app.vercel.app/
---------------------------------------------------------------------
"""

# =============================================================================
# RUNNING AND TESTING OUR CODE
# =============================================================================
if __name__ == "__main__":
    print("--- STEP 1: Understanding vercel.json ---")
    print(json.dumps(VERCEL_CONFIG, indent=2))

    print("\n--- STEP 2: Deploying to Vercel ---")
    print(VERCEL_STEPS.strip())

    print("\n" + "=" * 60)
    print("CONGRATULATIONS! You have completed all 26 Modules!")
    print("You now have a complete, progressive, module-by-module foundation")
    print("in Python, Flask, Databases, REST APIs, and Cloud Deployment!")
    print("=" * 60)
