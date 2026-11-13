
from flask import Blueprint, request, abort, make_response, Response
from app.db import db
from app.models.task import Task
from app.routes.route_utilities import validate_model
from datetime import datetime, timezone
import requests
import os


bp = Blueprint("tasks_bp", __name__)


def send_slack_notification(message):
    slack_token = os.environ.get("SLACK_BOT_TOKEN")

    if slack_token:
        url = "https://slack.com/api/chat.postMessage"

        headers = {
            "Authorization": f"Bearer {slack_token}"
        }

        data = {
            "channel": "task-notifications",
            "text": message
        }

        try:
            response = requests.post(
                url,
                headers=headers,
                json=data,
                timeout=10
            )

            response.raise_for_status()

            if not response.json().get("ok"):
                print("Slack error:", response.json().get("error"))

        except requests.RequestException as error:
            print("Slack request failed:", error)


@bp.post("/tasks")
def create_task():
    data = request.get_json()

    if not isinstance(data, dict):
        abort(make_response(
            {"details": "Invalid data"}, 400
        ))

    if not data.get("title") or not data.get("description"):
        abort(make_response(
            {"details": "Invalid data"}, 400
        ))

    task = Task.from_dict(data)

    db.session.add(task)
    db.session.commit()

    return task.to_dict(), 201


@bp.get("/tasks")
def get_tasks():
    sort_order = request.args.get("sort")

    query = db.select(Task)

    if sort_order == "asc":
        query = query.order_by(Task.title.asc())

    elif sort_order == "desc":
        query = query.order_by(Task.title.desc())

    tasks = db.session.execute(query).scalars()

    result = []

    for task in tasks:
        result.append(task.to_dict())

    return result, 200


@bp.get("/tasks/<int:task_id>")
def get_task(task_id):
    task = validate_model(Task, task_id)

    return task.to_dict(include_goal=task.goal_id is not None), 200


@bp.put("/tasks/<int:task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)

    data = request.get_json()

    if not isinstance(data, dict):
        abort(make_response(
            {"details": "Invalid data"}, 400
        ))

    if "title" in data:
        task.title = data["title"]

    if "description" in data:
        task.description = data["description"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.delete("/tasks/<int:task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.patch("/tasks/<int:task_id>/mark_complete")
def mark_complete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = datetime.now(timezone.utc)
    db.session.commit()

    message = f"Someone just completed the task {task.title}!"
    send_slack_notification(message)

    return Response(status=204, mimetype="application/json")


@bp.patch("/tasks/<int:task_id>/mark_incomplete")
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None
    db.session.commit()

    return Response(status=204, mimetype="application/json")
