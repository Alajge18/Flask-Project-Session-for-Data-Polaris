# Module 13 — HTML Forms

---

## Module 13 Syllabus Checklist

| # | Topic | Status |
|---|-------|--------|
| 1 | HTML form creation | Covered below |
| 2 | GET vs POST forms | Covered below |
| 3 | Form submission | Covered below |
| 4 | Form data / `request.form` | Covered below |
| 5 | Redirects | Covered below |
| 6 | Flash messages | Covered below |
| 7 | Post/Redirect/Get pattern | Covered below |

---

## A. Concept Explanation — What are HTML Forms?

### The Paper Form Analogy

Think of a paper form at a doctor's office. You fill in fields (name, phone, address), then hand it to the receptionist. The receptionist reads the data and processes it.

**HTML forms work the same way:**
- The **form** is the HTML page with input fields.
- The **user** fills in the fields and clicks Submit.
- The **browser** sends the data to Flask.
- **Flask** reads the data and does something with it (saves to database).

---

## B. GET vs POST

| Feature | GET | POST |
|---------|-----|------|
| **Where data goes** | In the URL: `/search?q=flask` | In the request body (hidden) |
| **Visible in URL?** | Yes | No |
| **Use for** | Searching, filtering | Creating, editing, deleting |
| **Bookmarkable?** | Yes | No |
| **Safe to repeat?** | Yes | No (might duplicate data) |

**Rule of thumb**: Use GET for reading data, POST for writing data.

---

## C. Code Implementation — Add Task Form

### The HTML Template ([add_task.html](file:///c:/Users/chaud/Desktop/Projects/Data%20polaris/task%20management%20system%20by%20me/TaskFlow/templates/add_task.html))

```html
<form method="POST">
    {{ form.hidden_tag() }}           <!-- CSRF token for security -->

    <div class="form-group">
        {{ form.title.label }}         <!-- <label>Title</label> -->
        {{ form.title(size=40) }}      <!-- <input type="text" size="40"> -->
        {% for error in form.title.errors %}
            <span class="error">{{ error }}</span>  <!-- Validation error -->
        {% endfor %}
    </div>

    <!-- ... more fields ... -->

    {{ form.submit(class="btn") }}     <!-- <button>Add Task</button> -->
</form>
```

**Key parts explained:**

| Code | What it renders | Why |
|------|----------------|-----|
| `method="POST"` | Form sends data in request body | Hides data from URL, safer for writes |
| `{{ form.hidden_tag() }}` | Hidden CSRF token field | Prevents fake form submissions |
| `{{ form.title.label }}` | `<label>Title</label>` | Labels tell users what to type |
| `{{ form.title(size=40) }}` | `<input type="text">` | The actual input field |
| `{% for error in form.title.errors %}` | Error messages in red | Shows why validation failed |

### The Flask Route ([app.py](file:///c:/Users/chaud/Desktop/Projects/Data%20polaris/task%20management%20system%20by%20me/TaskFlow/app.py))

```python
@app.route("/tasks/add", methods=["GET", "POST"])
def add_task():
    form = AddTaskForm()                    # Create form instance
    
    if form.validate_on_submit():           # POST + validation passed?
        create_task(                        # Save to database
            form.title.data,
            form.description.data,
            form.status.data
        )
        flash("Task created!", "success")   # Show success message
        return redirect(url_for("tasks"))   # Go to task list
    
    return render_template("add_task.html", form=form)  # Show the form
```

**Line-by-line:**

| Line | What it does |
|------|-------------|
| `methods=["GET", "POST"]` | This route accepts both GET (show form) and POST (process form) |
| `form = AddTaskForm()` | Creates the form object with all fields and validators |
| `form.validate_on_submit()` | Returns True only if: it's a POST AND all validators passed |
| `form.title.data` | Gets the value the user typed in the title field |
| `flash("Task created!", "success")` | Stores a one-time message to show on the next page |
| `redirect(url_for("tasks"))` | Sends the browser to `/tasks` |
| Last `render_template` | Runs on GET request, or when validation fails |

---

## D. The Post/Redirect/Get Pattern

### What is it?

After a successful form submission:
1. **POST** → User submits the form
2. **REDIRECT** → Flask sends the browser to a new page
3. **GET** → Browser loads the new page

### Why is it important?

Without redirect, if the user refreshes the page after submitting, the browser resends the POST request and creates a **duplicate entry**!

```
WITHOUT redirect:
  Submit form → Task created → User refreshes → Task created AGAIN! (duplicate)

WITH redirect (Post/Redirect/Get):
  Submit form → Task created → Redirect to /tasks → User refreshes → Just reloads /tasks (safe)
```

### Code pattern:

```python
if form.validate_on_submit():
    create_task(...)                      # 1. Save data
    flash("Task created!", "success")     # 2. Queue a message
    return redirect(url_for("tasks"))     # 3. Redirect (GET /tasks)
```

---

## E. Flash Messages

Flash messages are **one-time notifications**. They appear once, then disappear.

### Setting a flash message (in app.py):

```python
flash("Task created successfully!", "success")  # Green message
flash("Task not found.", "error")                # Red message
```

- First argument: the message text
- Second argument: the category (used for CSS styling)

### Displaying flash messages (in [base.html](file:///c:/Users/chaud/Desktop/Projects/Data%20polaris/task%20management%20system%20by%20me/TaskFlow/templates/base.html)):

```html
{% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
        {% for category, message in messages %}
            <div class="flash {{ category }}">{{ message }}</div>
        {% endfor %}
    {% endif %}
{% endwith %}
```

- `get_flashed_messages()` retrieves all queued messages
- `with_categories=true` gives us the category ("success"/"error")
- The message appears ONCE and is deleted after display

---

## F. Execution Flow — Form Submission

```
STEP 1: User visits /tasks/add (GET request)
  → Flask runs add_task()
  → form.validate_on_submit() returns False (it's GET, not POST)
  → Flask renders add_task.html with an empty form

STEP 2: User fills in the form and clicks "Add Task" (POST request)
  → Browser sends POST /tasks/add with form data in the body
  → Flask runs add_task() again
  → form.validate_on_submit() checks:
      ✓ Is it POST? Yes
      ✓ Is title filled? Yes
      ✓ Is user_id valid? Yes
      ✓ Is CSRF token correct? Yes
  → Returns True

STEP 3: Flask saves the task
  → create_task(...) inserts into database
  → flash("Task created!", "success") queues a message
  → redirect(url_for("tasks")) sends browser to /tasks

STEP 4: Browser loads /tasks (GET request)
  → Flask renders tasks.html
  → Flash message "Task created!" appears (green)
  → Next page load: message is gone
```

---

## G. Common Mistakes and Fixes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Forgetting `methods=["POST"]` | Form submit returns 405 Method Not Allowed | Add `methods=["GET", "POST"]` |
| Forgetting `{{ form.hidden_tag() }}` | CSRF validation fails, form won't submit | Add it inside every `<form>` |
| Not using redirect after POST | Refreshing page duplicates the action | Use `redirect(url_for(...))` |
| Forgetting `SECRET_KEY` | Flask-WTF throws an error | Set `app.config["SECRET_KEY"]` |
| Not displaying errors in template | User doesn't see why form failed | Add `{% for error in form.field.errors %}` |

---

## H. Practice Task

1. Try submitting the Add Task form with an empty title. Observe the validation error.
2. Submit a valid task. See the flash message appear, then refresh — it's gone.

---

## I. Teaching Questions

1. **"What's the difference between GET and POST?"**
   - GET puts data in the URL (for reading). POST puts data in the body (for writing).

2. **"Why do we redirect after a successful form submit?"**
   - To prevent duplicate submissions when the user refreshes.

3. **"What does `flash()` do?"**
   - Stores a one-time message that appears on the next page load.

4. **"What is `{{ form.hidden_tag() }}`?"**
   - Adds a hidden CSRF token to prevent fake form submissions.

5. **"What does `validate_on_submit()` check?"**
   - That the request is POST, all validators passed, and CSRF token is valid.

---

## J. Module 13 Completion Checklist

| # | Syllabus Point | Status | Demonstrated |
|---|---------------|--------|-------------|
| 1 | HTML form creation | Done | add_task.html, edit_task.html |
| 2 | GET vs POST | Done | GET shows form, POST processes it |
| 3 | Form submission | Done | Browser sends POST to Flask |
| 4 | Form data | Done | `form.title.data` reads submitted value |
| 5 | Redirects | Done | `redirect(url_for("tasks"))` |
| 6 | Flash messages | Done | `flash("Task created!", "success")` |
| 7 | Post/Redirect/Get | Done | Redirect after successful POST |

**All 7 syllabus points for Module 13 are covered.**
