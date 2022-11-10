from flask import Blueprint, jsonify, request, abort, make_response
from app.models.task import Task
from app import db
from datetime import datetime
import requests, os

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


# POST route
@task_bp.route("", methods=["POST"])
def create_one_task():
    request_body = request.get_json()

    try:
        new_task = Task.from_dict(request_body)
    except KeyError:
        return abort(make_response(jsonify({"details": "Invalid data"}), 400))

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": new_task.to_dict()}), 201


# GET routes
@task_bp.route("", methods=["GET"])
def get_all_tasks():

    sort_query_value = request.args.get("sort")

    if sort_query_value == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif sort_query_value == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
    
    tasks_response = [task.to_dict() for task in tasks]

    return jsonify(tasks_response), 200


@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_model_by_id(Task, task_id)

    return jsonify({"task": task.to_dict()}), 200


# PUT route
@task_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    update_task = validate_model_by_id(Task, task_id)
    request_body = request.get_json()
    
    try:
        update_task.title = request_body["title"]
        update_task.description = request_body["description"]
    except KeyError:
        return jsonify({"message":"KeyError: missing data needed"}),400

    db.session.commit()

    return jsonify({"task": update_task.to_dict()}), 200


# PATCH routes
@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def update_task_completion(task_id):
    task_to_patch = validate_model_by_id(Task, task_id)
    task_to_patch.completed_at = datetime.today()

    post_to_slack(task_to_patch)

    db.session.commit()
    
    return jsonify({"task": task_to_patch.to_dict()}), 200

def post_to_slack(task):
    path= "https://slack.com/api/chat.postMessage"
    query_params={
        "channel":"task_notifications", 
        "text":f"Someone just completed the task {task.title}"}
    slack_token = os.environ.get("SLACK_BOT_TOKEN")
    headers={"Authorization":slack_token}

    response = requests.post(url=path, data=query_params, headers=headers)
    print(response)

    return response


@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def update_task_incomplete(task_id):
    task_to_patch = validate_model_by_id(Task, task_id)
    task_to_patch.completed_at = None
        
    db.session.commit()

    return jsonify({"task": task_to_patch.to_dict()}), 200


# DELETE route
@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model_by_id(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({
        "details": f'Task {task.task_id} "{task.title}" successfully deleted'
    }), 200)


# Helper function
def validate_model_by_id(cls, model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        response_str = f"Invalid id: {model_id}. ID must be an integer."
        abort(make_response(jsonify({"message": response_str}), 400))

    requested_object = cls.query.get(model_id)

    if not requested_object:
        response_str = f"{cls.__name__} with id: {model_id} was not found in the database."
        abort(make_response(jsonify({"message": response_str}), 404))

    return requested_object