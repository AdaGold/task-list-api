from datetime import datetime
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort
from sqlalchemy import desc
import requests, os

tasks_bp = Blueprint("task", __name__, url_prefix="/tasks")

# HELPER FUNCTIONS
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} is not a valid id"}, 400))

    model = cls.query.get(model_id)
    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404))
    
    return model

def validate_request(request_body):
    try:
        request_body["title"]
        request_body["description"]
    except:
        abort(make_response({"details": "Invalid data"}, 400))

def post_to_slack(task_info):
    URL = "https://slack.com/api/chat.postMessage"
    QUERY_PARAMS = {
        "channel": "task-notifications", 
        "text": f"Someone just completed the task {task_info['title']}"
        }
    AUTHORIZATION = os.environ.get("SLACK_OAUTH_TOKEN")
    requests.post(URL, params=QUERY_PARAMS, headers = {"Authorization": AUTHORIZATION}
    )    

# CREATE
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    validate_request(request_body)
    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    created_task = {"task": new_task.to_dict()}
    return make_response(created_task, 201)

# READ
@tasks_bp.route("", methods=["GET"])
def handle_tasks():
    sort_query = request.args.get("sort")
    
    task_query = Task.query

    if sort_query == "asc":
        task_query = task_query.order_by(Task.title)
    
    if sort_query == "desc":
        task_query = task_query.order_by(desc(Task.title))

    tasks = task_query.all()
    response_body = [task.to_dict() for task in tasks]

    return jsonify(response_body), 200

@tasks_bp.route("/<task_id>", methods=["GET"])
def handle_one_task(task_id):
    task = validate_model(Task, task_id)
    
    response_body = {"task": task.to_dict()}

    return jsonify(response_body), 200

# UPDATE
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    response_body = {"task": validate_model(Task, task_id).to_dict()}

    return make_response(jsonify(response_body)), 200

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def complete_task(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = datetime.now()
    task.is_complete = True

    db.session.commit()

    completed_task = validate_model(Task, task_id).to_dict()
    response_body = {"task": completed_task}

    post_to_slack(completed_task)

    return make_response(jsonify(response_body)), 200

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def incomplete_task(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None
    task.is_complete = False

    db.session.commit()

    response_body = {"task": validate_model(Task, task_id).to_dict()}

    return make_response(jsonify(response_body)), 200

# DELETE
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)
    response_body = f"Task {task_id} \"{task.title}\" successfully deleted"

    db.session.delete(task)
    db.session.commit()
    
    return make_response({"details": response_body}, 200)