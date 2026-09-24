"""
=============================================================================
MODULE 25: Deploying Flask to Render
Project Story: Launching our "Task Manager" Live on the Web (Step 15)
=============================================================================
Previously in Module 24:
We pushed our project files to GitHub.

Now in Module 25:
We take our Task Manager and deploy it LIVE to the internet on Render!
Render is a cloud hosting platform that connects to GitHub and automatically
builds and hosts your Flask app for free.

Why Gunicorn?
Flask's built-in development server (app.run) is designed only for local testing.
In production, we use a production server called GUNICORN.

What is a Procfile?
A simple one-line text file named 'Procfile' (with no extension) that tells Render
how to start your app:
    web: gunicorn app:app

What you will learn in this module:
1. Adding gunicorn to requirements.txt
2. Creating a Procfile
3. Step-by-step walkthrough to deploy on dashboard.render.com

Next Module Connection:
In Module 26 (Final Module!), we will explore Serverless deployment on Vercel!
=============================================================================
"""

# =============================================================================
# 1. WHAT RENDER NEEDS IN YOUR REPOSITORY
# =============================================================================
REQUIRED_FILES = """
Your GitHub repository must have these 2 files in the root folder:

File 1: requirements.txt
------------------------
Flask==3.1.1
Flask-WTF==1.2.2
gunicorn==23.0.0

File 2: Procfile
------------------------
web: gunicorn app:app
"""

# =============================================================================
# 2. STEP-BY-STEP DEPLOYMENT GUIDE ON RENDER
# =============================================================================
RENDER_STEPS = """
---------------------------------------------------------------------
HOW TO DEPLOY ON RENDER (3 SIMPLE STEPS):
---------------------------------------------------------------------
1. Go to https://dashboard.render.com (Sign in with your GitHub account).
2. Click "New +" and select "Web Service".
3. Select your GitHub repository:
   - Name         : my-taskflow-app
   - Environment  : Python 3
   - Build Command: pip install -r requirements.txt
   - Start Command: gunicorn app:app
4. Click "Deploy Web Service"!
   In 2 minutes, Render will give you a live URL:
   https://my-taskflow-app.onrender.com/
---------------------------------------------------------------------
"""

# =============================================================================
# RUNNING AND TESTING OUR CODE
# =============================================================================
if __name__ == "__main__":
    print("--- STEP 1: Required Deployment Files ---")
    print(REQUIRED_FILES.strip())

    print("\n--- STEP 2: Step-by-Step Render Deployment ---")
    print(RENDER_STEPS.strip())

    print("\n[NEXT STEP] In Module 26, we will see how Serverless deployment works on Vercel!")
