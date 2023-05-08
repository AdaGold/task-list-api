from os import abort
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request

# Instantiate Blueprint instances here
tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if not "title" in request_body or not "description" in request_body:
        abort(make_response({"details": "Invalid data"}, 400))

    new_task = Task(title=request_body["title"],
                    description=request_body["description"])

    if new_task.completed_at:
        completed = True
    else:
        completed = False

    db.session.add(new_task)
    db.session.commit()

    # return make_response(jsonify(f"Task {new_task.title} successfully created"), 201)
    return make_response(jsonify({
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": completed

        }
    }), 201)
