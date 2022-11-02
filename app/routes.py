from flask import Blueprint, jsonify, request
from app.models.task import Task
from app import db

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@task_bp.route("", methods=["POST"])
def create_one_task():
    request_body = request.get_json()

    new_task = Task(
        title=request_body["title"],
        description=request_body["description"],
        completed_at=request_body["completed_at"]
    )
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": {
        "task_id": new_task.task_id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": False
    }}), 201
