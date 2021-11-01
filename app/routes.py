from app import db
from app.models.task import Task
from flask import Blueprint, request, jsonify
from datetime import datetime
import os
import requests

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["GET", "POST"])
def tasks():
    if request.method == "GET":
        sort_query = request.args.get("sort")
        if sort_query == "asc":
            tasks = Task.query.order_by(Task.title)
        elif sort_query == "desc":
            tasks = Task.query.order_by(Task.title.desc())
        else:
            tasks = Task.query.all()
        response_body = [task.to_dict() for task in tasks]
        return jsonify(response_body), 200

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

@tasks_bp.route("/<id>", methods=["GET", "PUT", "DELETE"])
@tasks_bp.route("/<id>/<status>", methods=["PATCH"])
def tasks_id(id, status=None):
    task = Task.query.get(id)
    if not task:
        return jsonify(None), 404

    if request.method == "GET":
        response_body = {
            "task": task.to_dict()
        }

    elif request.method == "PUT":
        request_body = request.get_json()
        task.title = request_body["title"]
        task.description = request_body["description"]
        task.completed_at = request_body.get("completed_at")

        db.session.commit()

        response_body = {
            "task": task.to_dict()
        }

    elif request.method == "PATCH":
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

        db.session.commit()

        response_body = {
            "task": task.to_dict()
        }

    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()

        response_body = {
            "details": f"Task {task.id} \"{task.title}\" successfully deleted"
        }

    return jsonify(response_body), 200
