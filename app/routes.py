import os
from app import db
import requests
from datetime import date
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request

tasks_bp = Blueprint('tasks_bp', __name__, url_prefix='/tasks')
root_bp = Blueprint("root_bp", __name__)

# Home page
@root_bp.route("/", methods=["GET"])
def root():
    return {
        "name": "Ghameerah's Task List API",
        "message": "Fun with Flask",
    }

# Get all tasks
@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    sort_method = request.args.get('sort')

    if not sort_method:
        tasks = Task.query.all()
    elif sort_method == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort_method == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_json())

    return jsonify(tasks_response)

# Create a task
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if not "title" in request_body or not "description" in request_body:  # or \
        # not "completed_at" in request_body:
        return jsonify({
            "details": "Invalid data"
        }), 400

    new_task = Task(title=request_body["title"],
                    description=request_body["description"])
    
    if "completed_at" in request_body:
        new_task.completed_at = request_body["completed_at"]

    db.session.add(new_task)
    db.session.commit()

    return {
        "task": new_task.to_json()
    }, 201

# Get one task
@tasks_bp.route("/<task_id>", methods=["GET"])
def read_single_task(task_id):
    task = Task.query.get(task_id)

    if task:
        return {
            "task": task.to_json()
        }
    else:
        return {"message": f"Task {task_id} not found"}, 404

# Update a task
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return {"message": f"Task {task_id} not found"}, 404

    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]
    # if request_body["completed_at"]:
    #     task.completed_at = datetime.utcnow

    db.session.add(task)
    db.session.commit()

    return {
        "task": task.to_json()
    }, 200

# Delete a task
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return {"message": f"Task {task_id} not found"}, 404

    db.session.delete(task)
    db.session.commit()

    return {
        "details": f"Task {task_id} \"{task.title}\" successfully deleted"
    }, 200
