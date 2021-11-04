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
        return f(*args, task=task, **kwargs)
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
    return jsonify([task.to_dict() for task in tasks])


@tasks_bp.route("", methods=["POST"])
def create_new_task():
    request_body = request.get_json()

    if not request_body.get("title") or "description" not in request_body or \
            "completed_at" not in request_body or len(request_body) != 3:
        return {"details": "Invalid data"}, 400

    new_task = Task.from_dict(request_body)
    db.session.add(new_task)
    db.session.commit()
    return response(new_task), 201


@tasks_bp.route("/<id>", methods=["GET"])
@validate_task
def get_one_task(task):
    return response(task)


@tasks_bp.route("/<id>", methods=["PUT"])
@validate_task
def edit_one_task(task):
    request_body = request.get_json()
    if not request_body.get("title"):
        return details(invalid_msg), 400
    task.edit(request_body)
    db.session.commit()
    return response(task)


@tasks_bp.route("/<id>", methods=["DELETE"])
@validate_task
def delete_one_task(task):
    db.session.delete(task)
    db.session.commit()
    return details(delete_msg(task))


@tasks_bp.route("/<id>/<status>", methods=["PATCH"])
@validate_task
def change_one_task_status(task, status):

    if status == "mark_complete":
        task.completed_at = datetime.now()
        send_slack_msg(task)

    elif status == "mark_incomplete":
        task.completed_at = None

    else:
        return jsonify(None), 404

    db.session.commit()
    return response(task)


def response(task):
    return {"task": task.to_dict()}


def details(msg):
    return {"details": msg}


def delete_msg(task):
    return f'Task {task.id} "{task.title}" successfully deleted'


def invalid_msg():
    return "Invalid data"


def send_slack_msg(task):
    data = {
        "token": os.environ.get("SLACK_BOT_TOKEN"),
        "channel": "task-notifications",
        "text": f"Someone just complete the task {task.title}"
    }
    requests.post("https://slack.com/api/chat.postMessage", data=data)