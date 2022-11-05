from flask import Blueprint, jsonify, request, abort, make_response
from app.models.task import Task
from app import db

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@task_bp.route("", methods=["POST"])
def create_one_task():
    request_body = request.get_json()
    
    try:
        new_task = Task(
                title=request_body["title"],
                description=request_body["description"]
                )
    except KeyError:
        return jsonify({"details": "Invalid data"}), 400

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": new_task.to_dict()}), 201


@task_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks = Task.query.all()

    tasks_response = [task.to_dict() for task in tasks]

    return jsonify(tasks_response), 200


@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task_by_id(task_id)

    return jsonify({"task": task.to_dict()}), 200


@task_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    update_task = validate_task_by_id(task_id)
    request_body = request.get_json()

    update_task.title = request_body["title"]
    update_task.description = request_body["description"]

    db.session.commit()

    return jsonify({"task": update_task.to_dict()}), 200

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task_by_id(task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({
        "details": f'Task {task.task_id} "{task.title}" successfully deleted'
        }))


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