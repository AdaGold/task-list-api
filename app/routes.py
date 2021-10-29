from app import db
from app.models.task import Task
from flask import Blueprint, request, jsonify

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["GET", "POST"])
def tasks():
    if request.method == "GET":
        tasks = Task.query.all()
        response = [task.to_dict() for task in tasks]
        return jsonify(response), 200

    elif request.method == "POST":
        request_body = request.get_json()

        if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
            return {"details": "Invalid data"}, 400

        task = Task.from_dict(request_body)

        db.session.add(task)
        db.session.commit()

        response_body={
            "task": task.to_dict()
        }

        return jsonify(response_body), 201
