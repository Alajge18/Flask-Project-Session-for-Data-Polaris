"""
=============================================================================
MODULE 02: Modules and Packages
Topic: Code Organization and Dependency Management (Foundation Phase)
=============================================================================
Welcome to Module 02!
In this module, we learn how Python organizes code across multiple files
and how to manage external dependencies.

What you will learn in this module:
1. What a Module is (any Python file ending with .py)
2. The 'import' statement (importing from other files and standard library)
3. Using Python's built-in modules (datetime, math)
4. What Packages and pip are
5. Virtual environments (venv) and requirements.txt
=============================================================================
"""

# =============================================================================
# 1. IMPORTING FROM PYTHON BUILT-IN STANDARD LIBRARY
# =============================================================================
# Python comes with many modules pre-installed!
import math
from datetime import datetime

# =============================================================================
# 2. IMPORTING FROM A LOCAL FILE (OUR OWN MODULE: calculator.py)
# =============================================================================
try:
    from calculator import add, multiply, COMPANY_NAME
except ImportError:
    from Module_Code.calculator import add, multiply, COMPANY_NAME


# =============================================================================
# 3. EXPLAINING VIRTUAL ENVIRONMENTS & PIP FOR BEGINNERS
# =============================================================================
DEPENDENCY_NOTES = """
---------------------------------------------------------------------
QUICK GUIDE: VIRTUAL ENVIRONMENTS (venv) & PIP
---------------------------------------------------------------------
1. What is pip?
   - The package installer for Python (like an App Store for Python code).
   - Example: pip install Flask

2. What is a Virtual Environment (venv)?
   - An isolated sandbox folder for your project so different projects
     don't conflict with different versions of libraries.
   - Creating venv:   python -m venv venv
   - Activating venv:
       Windows:       venv\\Scripts\\activate
       Mac/Linux:     source venv/bin/activate

3. What is requirements.txt?
   - A text file listing all packages your project needs.
   - Generate:        pip freeze > requirements.txt
   - Install all:     pip install -r requirements.txt
---------------------------------------------------------------------
"""


# =============================================================================
# DEMONSTRATION
# =============================================================================
if __name__ == "__main__":
    print("--- 1. Using Built-in Standard Library Modules ---")
    print("Square root of 16 using 'math.sqrt':", math.sqrt(16))
    print("Current timestamp using 'datetime.now':", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    print("\n--- 2. Using Our Custom Module (calculator.py) ---")
    print(f"Imported from {COMPANY_NAME}:")
    print("10 + 25 =", add(10, 25))
    print("6 * 7   =", multiply(6, 7))

    print(DEPENDENCY_NOTES)

    print("[NOTE] In Modules 01-10, we learn foundational concepts.")
    print("Our hands-on Project Implementation officially starts in Module 11!")
