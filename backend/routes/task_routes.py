# routes/task_routes.py
# ============================================
# Task Management Routes
# Full CRUD + Pagination + Dashboard stats
# ============================================

from flask import Blueprint, request, jsonify
import jwt
from models import (
    create_task, get_all_tasks, get_tasks_paginated, get_task_by_id,
    update_task, delete_task, toggle_task_status, get_dashboard_stats
)
from config import Config

task_bp = Blueprint("tasks", __name__)


# --------------------------------------------------
# Helper: Extract user_id from JWT token
# --------------------------------------------------
def get_current_user():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None
    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        return payload.get("user_id")
    except jwt.PyJWTError:
        return None


# --------------------------------------------------
# GET /dashboard
# --------------------------------------------------
@task_bp.route("/dashboard", methods=["GET"])
def dashboard():
    user_id = get_current_user()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    stats = get_dashboard_stats(user_id)
    return jsonify({"stats": stats}), 200


# --------------------------------------------------
# POST /tasks
# Create a new task
# --------------------------------------------------
@task_bp.route("/tasks", methods=["POST"])
def add_task():
    user_id = get_current_user()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    data        = request.get_json()
    title       = data.get("title", "").strip()
    if not title:
        return jsonify({"error": "Task title is required"}), 400

    description = data.get("description", "")
    priority    = data.get("priority", "Medium")
    due_date    = data.get("due_date") or None

    if priority not in ["Low", "Medium", "High"]:
        return jsonify({"error": "Priority must be Low, Medium, or High"}), 400

    task_id = create_task(title, description, priority, due_date, user_id)
    return jsonify({"message": "Task created successfully", "task_id": task_id}), 201


# --------------------------------------------------
# GET /tasks
# Get tasks with pagination support.
# Query params:
#   page    (int, default 1)
#   per_page (int, default 10)
#   status  ("Pending" | "Completed" | omit for all)
#
# Also supports ?all=true to return the full list
# (used for CSV / JSON export on the frontend)
# --------------------------------------------------
@task_bp.route("/tasks", methods=["GET"])
def get_tasks():
    user_id = get_current_user()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    # ?all=true → return every task (for export)
    if request.args.get("all") == "true":
        tasks = get_all_tasks(user_id)
        return jsonify({"tasks": tasks}), 200

    # Pagination parameters
    try:
        page     = int(request.args.get("page",     1))
        per_page = int(request.args.get("per_page", 10))
    except ValueError:
        return jsonify({"error": "page and per_page must be integers"}), 400

    page     = max(1, page)          # never below 1
    per_page = max(1, min(per_page, 100))  # clamp between 1 and 100

    status_filter = request.args.get("status")  # optional

    result = get_tasks_paginated(user_id, page, per_page, status_filter)
    return jsonify(result), 200


# --------------------------------------------------
# GET /tasks/<id>
# --------------------------------------------------
@task_bp.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    user_id = get_current_user()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    task = get_task_by_id(task_id, user_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"task": task}), 200


# --------------------------------------------------
# PUT /tasks/<id>
# --------------------------------------------------
@task_bp.route("/tasks/<int:task_id>", methods=["PUT"])
def edit_task(task_id):
    user_id  = get_current_user()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    existing = get_task_by_id(task_id, user_id)
    if not existing:
        return jsonify({"error": "Task not found"}), 404

    data        = request.get_json()
    title       = data.get("title",       existing["title"])
    description = data.get("description", existing["description"])
    priority    = data.get("priority",    existing["priority"])
    status      = data.get("status",      existing["status"])
    due_date    = data.get("due_date",    existing["due_date"]) or None

    if priority not in ["Low", "Medium", "High"]:
        return jsonify({"error": "Invalid priority"}), 400
    if status not in ["Pending", "Completed"]:
        return jsonify({"error": "Invalid status"}), 400

    success = update_task(task_id, user_id, title, description, priority, status, due_date)
    if success:
        return jsonify({"message": "Task updated successfully"}), 200
    return jsonify({"error": "Failed to update task"}), 500


# --------------------------------------------------
# DELETE /tasks/<id>
# --------------------------------------------------
@task_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
def remove_task(task_id):
    user_id = get_current_user()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    success = delete_task(task_id, user_id)
    if success:
        return jsonify({"message": "Task deleted successfully"}), 200
    return jsonify({"error": "Task not found"}), 404


# --------------------------------------------------
# PATCH /tasks/<id>/toggle
# --------------------------------------------------
@task_bp.route("/tasks/<int:task_id>/toggle", methods=["PATCH"])
def toggle_task(task_id):
    user_id = get_current_user()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    success = toggle_task_status(task_id, user_id)
    if success:
        return jsonify({"message": "Task status updated"}), 200
    return jsonify({"error": "Task not found"}), 404
