from app import db
from os import abort
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request

from datetime import datetime
import requests
import os
from dotenv import load_dotenv
load_dotenv()

# Instantiate Blueprint instances here
tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


SLACK_API_URL = "https://slack.com/api/chat.postMessage"
# SLACK_API_KEY = os.environ["SLACK_API_KEY"]
SLACK_API_KEY = os.environ.get("SLACK_API_KEY")

# *************************************************************************
# ********************************* TASKS *********************************
# *************************************************************************


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"details": f"Invalid data"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response(
            {"details": f"{cls.__name__} {model_id} not found"}, 404))

    return model


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if not "title" in request_body or not "description" in request_body:
        abort(make_response({"details": "Invalid data"}, 400))

    new_task = Task.from_dict(request_body)
    if new_task.completed_at:
        completed = True
    else:
        completed = False

    db.session.add(new_task)
    db.session.commit()

    # return make_response(jsonify(f"Task {new_task.title} successfully created"), 201)
    return make_response(jsonify({
        "task": new_task.to_dict()
    }), 201)


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():

    sort_type = request.args.get("sort")

    if sort_type == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort_type == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()

    task_response = []
    for task in tasks:
        task_response.append(
            task.to_dict()
        )
    return jsonify(task_response)


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_model(Task, task_id)

    return make_response(jsonify({
        "task": task.to_dict()
    }), 200)


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return make_response(jsonify({
        "task": task.to_dict()
    }), 200)


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(
        {"details": f"Task {task_id} \"{task.title}\" successfully deleted"}, 200)


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = Task.query.get(task_id)

    if not task:
        return {"details": f"Task {task_id} not found"}, 404

    task.completed_at = datetime.utcnow()

    db.session.add(task)
    db.session.commit()

    headers = {
        "Authorization": f"Bearer {SLACK_API_KEY}"
    }

    data = {
        "channel": "task-notifications",
        "text": f"Someone just completed the task: {task.title}"
    }

    result = {
        "task": task.to_dict()
    }

    r = requests.post(SLACK_API_URL, headers=headers, data=data)

    return make_response(jsonify(result), 200)


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = Task.query.get(task_id)

    if not task:
        return {"details": f"Task {task_id} not found"}, 404

    task.completed_at = None

    db.session.add(task)
    db.session.commit()

    if not task.completed_at:
        result = {
            "task": task.to_dict()}

    return make_response(jsonify(result), 200)
