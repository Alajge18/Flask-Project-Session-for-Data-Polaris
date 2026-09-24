"""
=============================================================================
MODULE 01: Functions and Scope
Topic: Python Programming Concepts (Foundation Phase)
=============================================================================
Welcome to Day 1!
In Modules 01 through 10, we focus on understanding core programming concepts
using simple, clear examples before starting our main project in Module 11.

What you will learn in this module:
1. Defining functions (def) with parameters and return values
2. Default arguments (parameters with fallback values)
3. Variable scope (Global vs Local variables)
4. *args (Passing a variable number of positional arguments)
5. **kwargs (Passing a variable number of keyword/named arguments)
=============================================================================
"""

# =============================================================================
# 1. SCOPE: GLOBAL VS LOCAL VARIABLES
# =============================================================================
# Global variable: Defined outside functions; accessible anywhere in the file.
app_name = "Python Learning Hub"
counter = 0

def demonstrate_scope():
    # Local variable: Defined inside this function; only exists while this function runs!
    local_message = "Hello from inside the function!"
    print(f"Inside function -> Global app_name: {app_name}")
    print(f"Inside function -> Local message: {local_message}")

# demonstrate_scope()
# print(local_message)  # -> This would cause an ERROR because local_message doesn't exist outside!


# =============================================================================
# 2. FUNCTION PARAMETERS, RETURN VALUES & DEFAULT ARGUMENTS
# =============================================================================
def calculate_bill(price, tax_rate=0.05, discount=0.0):
    """
    Calculates total bill.
    - 'price' is a REQUIRED parameter.
    - 'tax_rate' has a DEFAULT value of 0.05 (5%).
    - 'discount' has a DEFAULT value of 0.0.
    """
    tax_amount = price * tax_rate
    total = (price + tax_amount) - discount
    return total


# =============================================================================
# 3. *args (Variable Positional Arguments)
# =============================================================================
def sum_all_numbers(*numbers):
    """
    *numbers allows you to pass 2, 5, or 100 numbers.
    Python bundles all passed arguments into a tuple.
    """
    total = 0
    for num in numbers:
        total += num
    return total


# =============================================================================
# 4. **kwargs (Variable Keyword / Named Arguments)
# =============================================================================
def print_user_profile(username, **extra_details):
    """
    **extra_details allows passing arbitrary named arguments.
    Python bundles them into a dictionary.
    """
    print(f"User Profile: {username}")
    for key, value in extra_details.items():
        print(f"  - {key}: {value}")


# =============================================================================
# DEMONSTRATION
# =============================================================================
if __name__ == "__main__":
    print("--- 1. Variable Scope ---")
    demonstrate_scope()

    print("\n--- 2. Function with Default Arguments ---")
    # Using defaults (tax_rate=0.05, discount=0.0)
    bill1 = calculate_bill(100.0)
    print(f"Bill for $100 with default 5% tax: ${bill1:.2f}")

    # Overriding defaults
    bill2 = calculate_bill(100.0, tax_rate=0.10, discount=10.0)
    print(f"Bill for $100 with 10% tax and $10 discount: ${bill2:.2f}")

    print("\n--- 3. Using *args (Any number of arguments) ---")
    print("Sum of (5, 10):", sum_all_numbers(5, 10))
    print("Sum of (1, 2, 3, 4, 5):", sum_all_numbers(1, 2, 3, 4, 5))

    print("\n--- 4. Using **kwargs (Flexible details) ---")
    print_user_profile("alex99", role="Student", city="New York", course="Backend Python")

    print("\n[NOTE] In Modules 01-10, we learn foundational concepts.")
    print("Our hands-on Project Implementation officially starts in Module 11!")
