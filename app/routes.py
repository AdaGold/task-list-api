from flask import Blueprint, jsonify, request, abort, make_response
from app.models.task import Task
from app import db
from datetime import datetime


task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


# POST route
@task_bp.route("", methods=["POST"])
def create_one_task():
    request_body = request.get_json()

    try:
        new_task = Task.from_dict(request_body)
    except KeyError:
        return jsonify({"details": "Invalid data"}), 400

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
    task = validate_task_by_id(task_id)

    return jsonify({"task": task.to_dict()}), 200


# PUT route
@task_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    update_task = validate_task_by_id(task_id)
    request_body = request.get_json()

    update_task.title = request_body["title"]
    update_task.description = request_body["description"]

    db.session.commit()

    return jsonify({"task": update_task.to_dict()}), 200


# PATCH route
@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def update_task_completion(task_id):
    task_to_patch = validate_task_by_id(task_id)
    task_to_patch.completed_at = datetime.today()
        
    db.session.commit()

    return jsonify({"task": task_to_patch.to_dict()}), 200


# DELETE route
@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task_by_id(task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({
        "details": f'Task {task.task_id} "{task.title}" successfully deleted'
    }))


# Helper function
def validate_task_by_id(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        response_str = f"Invalid task_id: {task_id}. ID must be an integer."
        abort(make_response(jsonify({"message": response_str}), 400))

    requested_task = Task.query.get(task_id)

    if not requested_task:
        response_str = f"Task with id: {task_id} was not found in the database."
        abort(make_response(jsonify({"message": response_str}), 404))

    return requested_task