from flask import Blueprint, request, abort, make_response, Response
from .route_utilities import validate_model
from app.models.task import Task
from datetime import datetime
from ..db import db
import requests
import os


SLACK_API_URL = os.environ.get("SLACK_API_URL")
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")

bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@bp.get("")
def get_all_tasks():
    query = db.select(Task)
    sort_method = request.args.get('sort')

    if sort_method and sort_method == "asc":
        query = query.order_by(Task.title.asc())
    if sort_method and sort_method == "desc":
        query = query.order_by(Task.title.desc())

    tasks = db.session.scalars(query)
    tasks_response = [task.to_dict() for task in tasks]
    
    return tasks_response


@bp.post("")
def create_task():
    request_body = request.get_json()

    try:
        new_task = Task.from_dict(request_body)

    except KeyError as error:
        response = {"details": f"Invalid data"}
        abort(make_response(response, 400))

    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201


@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    return {"task": task.to_dict()}


@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.add(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.patch("/<task_id>/mark_complete")
def mark_task_complete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = datetime.now()

    db.session.add(task)
    db.session.commit()

    #post_to_slack(task)

    return Response(status=204, mimetype="application/json")


@bp.patch("/<task_id>/mark_incomplete")
def mark_task_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None

    db.session.add(task)
    db.session.commit()
    
    #post_to_slack(task)

    return Response(status=204, mimetype="application/json")


def post_to_slack(task):
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
    }
    if task.completed_at:
        data = {
            "channel": "instructors",
            "text": f"Task {task.title} has been marked complete",
        }
    else:
        data = {
            "channel": "general",
            "text": f"Task {task.title} has been marked incomplete",
        }

    r = requests.post(SLACK_API_URL, headers=headers, data=data)