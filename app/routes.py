from app import db
from app.models.task import Task
from flask import request, Blueprint, make_response, jsonify
from sqlalchemy import asc, desc

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods = ["POST"])
def add_task():
    """Adds new task to the Task table"""
    response_body = request.get_json()
    if len(response_body) != 3:
        return jsonify({"details": f"Invalid data"}), 400
    task = Task(
        title = response_body["title"],
        description = response_body["description"],
        completed_at = response_body["completed_at"]
        )  
    db.session.add(task)
    db.session.commit()
    return jsonify({"task": task.to_dict()}), 201

@tasks_bp.route("/<task_id>", methods=["GET"]) 
def get_one_task(task_id):
    """Gets data of a particular task"""
    task = Task.query.get(task_id)
    if not task:
        return jsonify(None), 404
    return jsonify({"task": task.to_dict()}), 200   

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    """Updates a portion of a single task"""
    task = Task.query.get(task_id)
    if not task:
        return jsonify(None), 404
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body["completed_at"]
    db.session.commit()
    return jsonify({"task": task.to_dict()}), 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    """Deletes one task from the Task table"""
    task = Task.query.get(task_id)
    if not task:
        return jsonify(None), 404
    db.session.delete(task)
    db.session.commit()
    return ({"details": f"Task {task_id} \"{task.title}\" successfully deleted"}, 200)

@tasks_bp.route("", methods=["GET"])
def get_tasks():
    """
    Returns an array of tasks.
    - No arg provided -> return all tasks
    - Arg provided -> return tasks sorted by title
    """
    task_order = request.args.get("sort")
    if task_order == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif task_order == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
    response_body = [] 
    for task in tasks:
        response_body.append(task.to_dict())
    return jsonify(response_body), 200