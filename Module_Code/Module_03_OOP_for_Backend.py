"""
=============================================================================
MODULE 03: Object-Oriented Programming (OOP) for Backend
Topic: Classes, Objects, Attributes, and Methods (Foundation Phase)
=============================================================================
Welcome to Module 03!
In backend development, data records (like users, products, or orders)
are modeled as Python Classes.

What you will learn in this module:
1. What a Class is (a blueprint for creating objects)
2. The __init__() constructor (initializes object attributes)
3. Instance attributes (data stored on an object: self.username, self.email)
4. Methods (functions that belong to an object)
5. Converting an object to a dictionary (to_dict()) for web responses
=============================================================================
"""

class User:
    """
    A simple class representing a User in a backend system.
    """
    def __init__(self, user_id, username, email):
        # Instance attributes
        self.id = user_id
        self.username = username
        self.email = email
        self.is_active = True

    # Instance method
    def deactivate(self):
        """Changes user status to inactive."""
        self.is_active = False
        print(f"User '{self.username}' has been deactivated.")

    # Method to format data as dictionary (useful for web APIs!)
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_active": self.is_active
        }


# =============================================================================
# DEMONSTRATION
# =============================================================================
if __name__ == "__main__":
    print("--- 1. Creating Objects from a Class (Instantiation) ---")
    user1 = User(1, "alice", "alice@example.com")
    user2 = User(2, "bob", "bob@example.com")

    print(f"User 1: ID={user1.id}, Name={user1.username}, Active={user1.is_active}")
    print(f"User 2: ID={user2.id}, Name={user2.username}, Active={user2.is_active}")

    print("\n--- 2. Calling Methods to Modify State ---")
    user2.deactivate()
    print("User 2 active status now:", user2.is_active)

    print("\n--- 3. Converting Object to Dictionary ---")
    print("User 1 Dictionary:", user1.to_dict())

    print("\n[NOTE] In Modules 01-10, we learn foundational concepts.")
    print("Our hands-on Project Implementation officially starts in Module 11!")
