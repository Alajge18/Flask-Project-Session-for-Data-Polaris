"""
=============================================================================
MODULE 04: Dictionaries and JSON Thinking
Topic: The Language of Web Data Exchange (Foundation Phase)
=============================================================================
Welcome to Module 04!
In web applications, Python backends process data as Dictionaries,
but browsers, mobile apps, and frontends communicate in JSON (plain text).

What you will learn in this module:
1. Python Dictionaries (key-value data records)
2. What JSON is (JavaScript Object Notation text)
3. json.dumps() -> Serialization: Python Dictionary -> JSON String (Sending data)
4. json.loads() -> Deserialization: JSON String -> Python Dictionary (Receiving data)
=============================================================================
"""

import json

# -----------------------------
# 1. Python Dictionary
# -----------------------------

student = {
    "id": 101,
    "name": "Devansh",
    "branch": "CSE",
    "skills": ["Python", "Flask", "SQL"],
    "is_admin": False
}

print("===== PYTHON DICTIONARY =====")
print(student)
print("Type:", type(student))


# -----------------------------
# 2. Dictionary → JSON
# -----------------------------

json_data = json.dumps(student, indent=2)

print("\n===== JSON DATA =====")
print(json_data)
print("Type:", type(json_data))


# -----------------------------
# 3. JSON → Dictionary
# -----------------------------

python_data = json.loads(json_data)

print("\n===== BACK TO PYTHON =====")
print(python_data)
print("Type:", type(python_data))


# -----------------------------
# 4. Access JSON-converted data
# -----------------------------

print("\n===== STUDENT INFORMATION =====")
print("Name:", python_data["name"])
print("Branch:", python_data["branch"])
print("First Skill:", python_data["skills"][0])
