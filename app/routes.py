from flask import Blueprint, jsonify, request
from app.models.task import Task
from app import db

task_bp = Blueprint("task", __name__, url_prefix="/task")

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
