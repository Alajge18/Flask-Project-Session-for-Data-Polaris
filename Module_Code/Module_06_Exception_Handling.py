"""
=============================================================================
MODULE 06: Exception Handling
Topic: Defensive Programming and Preventing Crashes (Foundation Phase)
=============================================================================
Welcome to Module 06!
In backend development, unexpected inputs (like invalid user data or missing records)
can cause errors. If unhandled, these errors crash your server!

What you will learn in this module:
1. What exceptions are and why they occur
2. Catching errors with try...except...finally
3. Raising exceptions intentionally with 'raise'
4. Defining a custom exception (e.g. InvalidAgeError)
=============================================================================
"""

# =============================================================================
# 1. CUSTOM EXCEPTION CLASS
# =============================================================================
class InvalidAgeError(Exception):
    """Raised when an age input is invalid."""
    pass


# =============================================================================
# 2. FUNCTION THAT VALIDATES INPUT AND RAISES EXCEPTIONS
# =============================================================================
def register_student(name, age):
    """
    Registers a student.
    Raises ValueError or InvalidAgeError if rules fail.
    """
    if not name or not isinstance(name, str):
        raise ValueError("Student name must be a non-empty string.")

    if age < 0 or age > 120:
        raise InvalidAgeError(f"Age {age} is not valid. Must be between 0 and 120.")

    return {"name": name, "age": age, "status": "Registered"}


# =============================================================================
# 3. DEFENSIVE CODING WITH TRY...EXCEPT...FINALLY
# =============================================================================
def safe_registration(name, age):
    try:
        student = register_student(name, age)
        print(f" [SUCCESS] Registered: {student['name']} (Age: {student['age']})")
        return student
    except ValueError as err:
        print(f" [ERROR - Invalid Input] {err}")
    except InvalidAgeError as err:
        print(f" [ERROR - Business Rule Failed] {err}")
    except Exception as unexpected:
        print(f" [UNEXPECTED ERROR] {unexpected}")
    finally:
        print(" [CLEANUP] Registration attempt completed.")


# =============================================================================
# DEMONSTRATION
# =============================================================================
if __name__ == "__main__":
    print("--- 1. Valid Input (Happy Path) ---")
    safe_registration("Emma Watson", 21)

    print("\n--- 2. Invalid Input (ValueError) ---")
    safe_registration("", 25)

    print("\n--- 3. Invalid Rule (Custom InvalidAgeError) ---")
    safe_registration("Benjamin Button", 150)

    print("\n[NOTE] Modules 07, 08, and 09 cover Web & HTTP theory in Preparation_guide/.")
    print("In Module 10, we introduce Flask.")
    print("Our hands-on Project Implementation officially starts in Module 11!")
