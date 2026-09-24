"""
=============================================================================
MODULE 24: Git and GitHub for Backend Developers
Project Story: Version Control for our "Task Manager" (Step 14)
=============================================================================
Previously in Module 23:
We secured our app with environment variables.

Now in Module 24:
We learn how to save our project versions using Git and push it to GitHub.

What is .gitignore?
A text file named exactly '.gitignore' that tells Git which files to NEVER
upload to GitHub:
1. venv/             -> Virtual environment (hundreds of MBs of local binaries)
2. __pycache__/      -> Python compiled cache files
3. .env              -> Secret keys and passwords
4. *.db              -> Local SQLite database files

What you will learn in this module:
- The 4 essential Git commands every beginner must know
- Creating and understanding the .gitignore file
- How cloud platforms use GitHub to deploy your code

Next Module Connection:
In Module 25, we will connect our GitHub repository to Render for live deployment!
=============================================================================
"""

# =============================================================================
# 1. THE STANDARD .gitignore CONTENT FOR FLASK
# =============================================================================
SAMPLE_GITIGNORE = """# Virtual Environment (Never commit this!)
venv/
env/

# Python Cache
__pycache__/
*.pyc

# Local Database Files
*.db
*.sqlite3

# Environment Secrets
.env
"""

# =============================================================================
# 2. THE 4 ESSENTIAL GIT COMMANDS
# =============================================================================
GIT_GUIDE = """
---------------------------------------------------------------------
THE 4 ESSENTIAL GIT COMMANDS:
---------------------------------------------------------------------
1. git init
   -> Initializes a new Git repository in your project folder.

2. git add .
   -> Stages all your project files (ignoring files in .gitignore).

3. git commit -m "Initial commit of Task Manager app"
   -> Takes a snapshot of your project with a descriptive message.

4. git push origin main
   -> Uploads your committed code to your GitHub repository!
---------------------------------------------------------------------
"""

# =============================================================================
# RUNNING AND TESTING OUR CODE
# =============================================================================
if __name__ == "__main__":
    print("--- STEP 1: Understanding .gitignore ---")
    print("Files you must NEVER push to GitHub:")
    print(SAMPLE_GITIGNORE.strip())

    print("\n--- STEP 2: The Core Git Commands ---")
    print(GIT_GUIDE.strip())

    print("\n[NEXT STEP] In Module 25, we deploy our GitHub repo to Render!")
