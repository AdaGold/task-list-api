from flask import Blueprint, request, Response
from datetime import datetime
import requests
import os
from app.models.task import Task
from app.db import db
from .routes_yay import validate_model, create_model

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

@task_bp.post("")
def create_task():
    request_body = request.get_json()
    return create_model(Task, request_body)

@task_bp.get("")
def get_all_tasks():
    query = db.select(Task)

    sort_param = request.args.get("sort")
    if sort_param == "asc":
        query = query.order_by(Task.title)
    elif sort_param == "desc":
        query = query.order_by(Task.title.desc())
    else:
        query = query.order_by(Task.id)

    tasks = db.session.scalars(query)

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    return tasks_response

@task_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    return task.to_dict()

@task_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@task_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@task_bp.patch("/<task_id>/mark_complete")
def mark_complete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = datetime.now()
    db.session.commit()

    slack_token = os.environ.get("SLACK_BOT_TOKEN")
    headers = {"Authorization": f"Bearer {slack_token}"}
    slack_data = {
        "channel": "api-testing",
        "text": f"Someone just completed the task {task.title}"
    }
    requests.post("https://slack.com/api/chat.postMessage", json=slack_data, headers=headers)

    return Response(status=204, mimetype="application/json")

@task_bp.patch("/<task_id>/mark_incomplete")
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None
    db.session.commit()

    return Response(status=204, mimetype="application/json")