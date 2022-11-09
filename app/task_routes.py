from app import db
from app.models.task import Task
from flask import Blueprint, request, make_response, jsonify, abort
import datetime
import os
import requests

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

# create helper function to post message to Slack
def slack_bot(slack_message):
    path = "https://slack.com/api/chat.postMessage"
    SLACK_API_KEY = os.environ.get("SLACK_API_KEY")
    HEADERS = {"Authorization": SLACK_API_KEY}
    channel_id ="C049QSML63U"
    
    query_params = {
        "channel": channel_id, 
        "text": slack_message
        }

    requests.post(path, params=query_params, headers=HEADERS)

# validate ids for models
def validate_id(cls, model_id):
    try: 
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))
    
    model = cls.query.get(model_id)
    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model

# validate request body information
def validate_request_body(cls, request_body):
    try:
        new_model = cls.from_dict(request_body)
    except:
        abort(make_response({"details":f"Invalid data"}, 400))

    return new_model

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    new_task = validate_request_body(Task, request_body)

    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify({"task": new_task.to_dict()}), 201)

@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()

    tasks_response = [task.to_dict() for task in tasks]

    return jsonify(tasks_response)

@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_id(Task, task_id)
    if not task.goal_id:
        response = {"task": task.to_dict()}
    else:
        response = {"task": task.to_dict_with_goal()}
    
    return make_response(jsonify(response))

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_id(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body.get("completed_at", None)
    
    db.session.commit()

    return make_response(jsonify({"task": task.to_dict()}))

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_id(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details":f"Task {task.task_id} \"{task.title}\" successfully deleted"})

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    task = validate_id(Task, task_id)
    task.completed_at = datetime.datetime.now()

    db.session.commit()

    slack_message = f"Someone just completed the task {task.title}"
    slack_bot(slack_message)

    return make_response(jsonify({"task": task.to_dict()}))

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    task = validate_id(Task, task_id)
    task.completed_at = None

    db.session.commit()

    return make_response(jsonify({"task": task.to_dict()}))