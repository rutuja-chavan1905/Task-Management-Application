# models.py
# ============================================
# Database Models (Helper Functions)
# Functions to interact with the database
# ============================================

from database import get_connection

# ==========================================
# USER MODEL
# ==========================================

def create_user(name, email, hashed_password):
    """Insert a new user into the users table."""
    conn   = get_connection()
    cursor = conn.cursor()
    query  = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, email, hashed_password))
    conn.commit()
    user_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return user_id


def get_user_by_email(email):
    """Find a user by their email address. Returns a dict or None."""
    conn   = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user


def get_user_by_id(user_id):
    """Find a user by their ID. Returns a dict or None."""
    conn   = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, email, created_at FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user


# ==========================================
# TASK MODEL
# ==========================================

def _serialize_task(task):
    """Convert date objects to strings so they can be sent as JSON."""
    if task:
        if task.get("due_date"):
            task["due_date"] = str(task["due_date"])
        if task.get("created_at"):
            task["created_at"] = str(task["created_at"])
    return task


def create_task(title, description, priority, due_date, user_id):
    """Insert a new task for a user."""
    conn   = get_connection()
    cursor = conn.cursor()
    query  = """
        INSERT INTO tasks (title, description, priority, due_date, user_id)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (title, description, priority, due_date, user_id))
    conn.commit()
    task_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return task_id


def get_all_tasks(user_id):
    """
    Get ALL tasks for a user (used for CSV/JSON export and dashboard charts).
    Returns full list without pagination.
    """
    conn   = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM tasks WHERE user_id = %s ORDER BY created_at DESC",
        (user_id,)
    )
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return [_serialize_task(t) for t in tasks]


def get_tasks_paginated(user_id, page=1, per_page=10, status_filter=None):
    """
    Get tasks with LIMIT / OFFSET for pagination.

    Args:
        user_id      : ID of the logged-in user
        page         : Current page number (1-based)
        per_page     : How many tasks per page (default 10)
        status_filter: "Pending" | "Completed" | None (all)

    Returns dict with:
        tasks      : list of task dicts for this page
        total      : total number of matching tasks
        page       : current page
        per_page   : page size
        total_pages: how many pages exist
    """
    conn   = get_connection()
    cursor = conn.cursor(dictionary=True)

    offset = (page - 1) * per_page   # e.g. page 2, per_page 10 → offset 10

    # Build WHERE clause dynamically based on optional status filter
    if status_filter and status_filter in ("Pending", "Completed"):
        where = "WHERE user_id = %s AND status = %s"
        params_count = (user_id, status_filter)
        params_page  = (user_id, status_filter, per_page, offset)
    else:
        where = "WHERE user_id = %s"
        params_count = (user_id,)
        params_page  = (user_id, per_page, offset)

    # Count total matching rows (needed to calculate total pages)
    cursor.execute(f"SELECT COUNT(*) AS total FROM tasks {where}", params_count)
    total = cursor.fetchone()["total"]

    # Fetch one page of tasks using LIMIT and OFFSET
    cursor.execute(
        f"SELECT * FROM tasks {where} ORDER BY created_at DESC LIMIT %s OFFSET %s",
        params_page
    )
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()

    import math
    return {
        "tasks"      : [_serialize_task(t) for t in tasks],
        "total"      : total,
        "page"       : page,
        "per_page"   : per_page,
        "total_pages": math.ceil(total / per_page) if total > 0 else 1
    }


def get_task_by_id(task_id, user_id):
    """Get a single task by its ID (only if it belongs to the user)."""
    conn   = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks WHERE id = %s AND user_id = %s", (task_id, user_id))
    task = cursor.fetchone()
    cursor.close()
    conn.close()
    return _serialize_task(task)


def update_task(task_id, user_id, title, description, priority, status, due_date):
    """Update an existing task."""
    conn   = get_connection()
    cursor = conn.cursor()
    query  = """
        UPDATE tasks
        SET title=%s, description=%s, priority=%s, status=%s, due_date=%s
        WHERE id=%s AND user_id=%s
    """
    cursor.execute(query, (title, description, priority, status, due_date, task_id, user_id))
    conn.commit()
    rows_affected = cursor.rowcount
    cursor.close()
    conn.close()
    return rows_affected > 0


def delete_task(task_id, user_id):
    """Delete a task (only if it belongs to the user)."""
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s AND user_id = %s", (task_id, user_id))
    conn.commit()
    rows_affected = cursor.rowcount
    cursor.close()
    conn.close()
    return rows_affected > 0


def toggle_task_status(task_id, user_id):
    """Toggle a task's status between Pending and Completed."""
    conn   = get_connection()
    cursor = conn.cursor()
    query  = """
        UPDATE tasks
        SET status = IF(status = 'Pending', 'Completed', 'Pending')
        WHERE id = %s AND user_id = %s
    """
    cursor.execute(query, (task_id, user_id))
    conn.commit()
    rows_affected = cursor.rowcount
    cursor.close()
    conn.close()
    return rows_affected > 0


def get_dashboard_stats(user_id):
    """Get task counts for the dashboard summary."""
    conn   = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total FROM tasks WHERE user_id = %s", (user_id,))
    total = cursor.fetchone()["total"]

    cursor.execute(
        "SELECT COUNT(*) AS completed FROM tasks WHERE user_id = %s AND status = 'Completed'",
        (user_id,)
    )
    completed = cursor.fetchone()["completed"]

    cursor.execute(
        "SELECT COUNT(*) AS pending FROM tasks WHERE user_id = %s AND status = 'Pending'",
        (user_id,)
    )
    pending = cursor.fetchone()["pending"]

    cursor.close()
    conn.close()
    return {"total": total, "completed": completed, "pending": pending}
