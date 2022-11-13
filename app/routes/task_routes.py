from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task
from datetime import datetime
import logging
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# ================================
# Create one task 
# ================================
@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    try:
        new_task = Task.create(request_body)
    except KeyError as error:
        return make_response({"details": "Invalid data"}, 400)

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": new_task.to_json()}), 201

# ==================================
# Get all tasks  
# ==================================
@task_bp.route("", methods=["GET"])
def get_all_tasks():
    sort_query = request.args.get("sort")
    if sort_query == 'asc':
        all_tasks = Task.query.order_by(Task.title.asc())
    elif sort_query == 'desc':
        all_tasks = Task.query.order_by(Task.title.desc())
    else:
        all_tasks = Task.query.all()
    
    results_list = []
    for task in all_tasks:
        results_list.append(task.to_json())

    return jsonify(results_list), 200

# ==================================
# Get one task by id number
# ==================================
@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    return jsonify({"task": validate_id(Task, task_id).to_json()}), 200

# ==================================
# Update one task 
# ==================================
@task_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    request_body = request.get_json()
    task = validate_id(Task, task_id)
    task.update(request_body)

    db.session.commit()

    return jsonify({"task": task.to_json()}), 200

# ==================================
# Delete one task by id
# ==================================
@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task = validate_id(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details":f'Task {task.task_id} "{task.title}" successfully deleted'}, 200)

# ==================================
# update one task's completeness
# ==================================
@task_bp.route("/<task_id>/<mark>", methods=["PATCH"])
def mark_tasks_complete_or_incomplete(task_id, mark):
    task = validate_id(Task, task_id)
    if mark == "mark_complete":
        send_to_slack(task.title, "task-notifications")
        task.completed_at = datetime.now()
        db.session.commit()
        return jsonify({"task": task.to_json()}), 200
    elif mark == "mark_incomplete":
        task.completed_at = None
        db.session.commit()
        return jsonify({"task": task.to_json()}), 200
# can combine this into one expression - ternary https://www.geeksforgeeks.org/ternary-operator-in-python/

# ==================================
# Helper function to validate id
# ==================================
def validate_id(class_name,id):
    try:
        id = int(id)
    except:
        abort(make_response({"message":f"Id {id} is an invalid id"}, 400))

    query_result = class_name.query.get(id)
    if not query_result:
        abort(make_response({"message":f"Id {id} not found"}, 404))

    return query_result

# ==================================
# Helper function to send message to slack
# ==================================
def send_to_slack(title, channel_name):
    client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
    logger = logging.getLogger(__name__)
    try:
    # Call the chat.postMessage method using the WebClient
        result = client.chat_postMessage(
            channel=channel_name, 
            text= f"Someone just completed the task '{title}'"
        )
        logger.info(result)

    except SlackApiError as e:
        logger.error(f"Error posting message: {e}")