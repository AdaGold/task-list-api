from flask import Blueprint, request, jsonify, make_response, abort
from app.models.task import Task
from app import db
from sqlalchemy import asc, desc
from datetime import datetime, timezone
import requests, os

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message":f"Task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message":f"Task {task_id} not found"}, 404))

    return task

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    sort_query = request.args.get("sort")
    tasks_query = Task.query

    if sort_query == "asc":
        tasks_query = Task.query.order_by(asc("title"))
    if sort_query == "desc":
        tasks_query = Task.query.order_by(desc("title"))

    tasks = tasks_query.all()
    tasks_response = [task.to_dict() for task in tasks]
    
    return jsonify(tasks_response), 200


@tasks_bp.route("/<id>", methods=["GET"])
def get_one_task(id):
    task = validate_task(id)

    return jsonify({"task":task.to_dict()}), 200


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        abort(make_response({"details": "Invalid data"}, 400))

    new_task = Task(title=request_body["title"],
                    description=request_body["description"])
    
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task":new_task.to_dict()}), 201


@tasks_bp.route("/<id>", methods=["PUT"])
def update_task(id):
    task = validate_task(id)
    request_body=request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return jsonify({"task":task.to_dict()}), 200


@tasks_bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    task = validate_task(id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({"details": f'Task {id} "{task.title}" successfully deleted'}), 200


########## Wave 3 ###########
def post_message_to_slack(task):
    SLACK_API_ROOT = "https://slack.com/api/chat.postMessage"
    CHANNEL_ID = os.environ.get("CHANNEL_ID")

    message = f"Someone just completed the task {task.title}"
    endpoint_url = SLACK_API_ROOT + "?channel=" + CHANNEL_ID + "&text=" + message

    response = requests.post(endpoint_url, headers={"Authorization": os.environ.get("SLACK_BOT_TOKEN")})

    # raises an error if status code is not 200
    response.raise_for_status()
    
    return response

@tasks_bp.route("/<id>/mark_complete", methods=["PATCH"])
def mark_task_complete(id):
    task = validate_task(id)

    task.completed_at = datetime.now(timezone.utc)
    db.session.commit()

    post_message_to_slack(task)

    return jsonify({"task":task.to_dict()}), 200


@tasks_bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(id):
    task = validate_task(id)

    task.completed_at = None
    db.session.commit()

    return jsonify({"task":task.to_dict()}), 200

########## Wave 4 ###########




