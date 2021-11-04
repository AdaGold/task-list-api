from app import db
from app.models.task import Task
from flask import Blueprint, request, jsonify
from datetime import datetime
import os
import requests
from functools import wraps


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


def validate_task(f):
    @wraps(f)
    def decorated_function(*args, id, **kwargs):
        task = Task.query.get(id)
        if not task:
            return jsonify(None), 404
        return f(*args, task, **kwargs)
    return decorated_function

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title)
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
    response_body = [task.to_dict() for task in tasks]
    return jsonify(response_body), 200

@tasks_bp.route("", methods=["POST"])
def create_new_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
        return {"details": "Invalid data"}, 400

    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    response_body={
        "task": new_task.to_dict()
    }

    return jsonify(response_body), 201

@tasks_bp.route("/<id>", methods=["GET"])
@validate_task
def get_one_task(task):
    return {
        "task": task.to_dict()
    }

@tasks_bp.route("/<id>", methods=["PUT"])
@validate_task
def edit_one_task(task):
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body.get("completed_at")

    db.session.commit()

    return {
        "task": task.to_dict()
    }

@tasks_bp.route("/<id>", methods=["DELETE"])
@validate_task
def delete_one_task(task):
    db.session.delete(task)
    db.session.commit()

    return {
        "details": f"Task {task.id} \"{task.title}\" successfully deleted"
    }


@tasks_bp.route("/<id>/<status>", methods=["PATCH"])
@validate_task
def change_one_task_status(task, status):

    if status == "mark_complete":
        task.completed_at = datetime.now()

        data = {
            "token": os.environ.get("SLACK_BOT_TOKEN"),
            "channel": "task-notifications",
            "text": f"Someone just complete the task {task.title}"
        }
        requests.post("https://slack.com/api/chat.postMessage", data=data)

    elif status == "mark_incomplete":
        task.completed_at = None

    else:
        return jsonify(None), 404

    db.session.commit()

    return {
        "task": task.to_dict()
    }

