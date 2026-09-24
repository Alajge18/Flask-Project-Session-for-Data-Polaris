"""
=============================================================================
MODULE 05: Python Decorators
Topic: Understanding the '@' Syntax Before Starting Flask (Foundation Phase)
=============================================================================
Welcome to Module 05!
In Flask, almost every route begins with a decorator:
    @app.route("/")
    def home(): ...

Many beginners find the '@' symbol confusing.
In Python, a DECORATOR is simply a function that takes another function as input,
adds some behavior before or after it, and returns it.

What you will learn in this module:
1. Functions are first-class citizens (functions can be passed as arguments)
2. Writing a simple decorator: @log_action
3. The '@' decorator syntax explained
4. How Flask uses this exact pattern for @app.route
=============================================================================
"""

# =============================================================================
# 1. WRITING A SIMPLE DECORATOR
# =============================================================================
def log_action(func):
    """
    A decorator that prints a message before and after the wrapped function runs.
    """
    def wrapper(*args, **kwargs):
        print(f"--> [LOG] Starting function: '{func.__name__}'")
        result = func(*args, **kwargs)
        print(f"--> [LOG] Finished function: '{func.__name__}' successfully!")
        return result
    return wrapper


# =============================================================================
# 2. APPLYING THE DECORATOR USING '@'
# =============================================================================
@log_action
def greet(name):
    print(f"    Hello, {name}! Welcome to Python Backend.")
    return f"Greeted {name}"


# =============================================================================
# 3. HOW FLASK USES THIS EXACT PATTERN (Mini Router Concept)
# =============================================================================
routes_table = {}

def my_route(url_path):
    """How Flask's @app.route works under the hood!"""
    def decorator(func):
        routes_table[url_path] = func
        return func
    return decorator

@my_route("/home")
def home_page():
    return "Welcome to the Homepage!"


# =============================================================================
# DEMONSTRATION
# =============================================================================
if __name__ == "__main__":
    print("--- 1. Testing Our Custom Decorator ---")
    greet("David")

    print("\n--- 2. How Flask Uses Decorators ---")
    print("Registered routes table:", routes_table)
    print("Executing function for '/home':", routes_table["/home"]())

    print("\n[NOTE] In Modules 01-10, we learn foundational concepts.")
    print("Our hands-on Project Implementation officially starts in Module 11!")
