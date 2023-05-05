from flask import Blueprint, jsonify, make_response, request, abort
from app import db
from app.models.task import Task
from datetime import datetime

task_bp = Blueprint("task", __name__, url_prefix="/tasks")
def validate_task(request_body):
    try:
        new_task = Task.from_dict(request_body)
    except KeyError:
        return abort(make_response({"details": "Invalid data"}, 400))
    return new_task

@task_bp.route("", methods=["POST"])
def create_one_task():
    request_body = request.get_json()
    new_task = validate_task(request_body)

    db.session.add(new_task)
    db.session.commit()

    return make_response({"task": new_task.to_dict()}, 201)

@task_bp.route("", methods=["GET"])
def get_all_tasks():
    response = []
    sort_query = request.args.get("sort")

    if sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    elif sort_query == "asc":
        tasks = Task.query.order_by(Task.title)
    else:
        tasks = Task.query.all()
    
    for task in tasks:
        response.append(task.to_dict())

    return jsonify(response), 200

def validate_id(cls, id):
    try:
        id = int(id)
    except:
        abort(make_response({"message": f"{cls.__name__} {id} invalid"}, 400))
    record = cls.query.get_or_404(id)
    return record

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_id(Task, task_id)
    return make_response({"task": task.to_dict()}, 200)

@task_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    task = validate_id(Task, task_id)
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()
    return make_response({"task": task.to_dict()}, 200)

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task = validate_id(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f"Task {task.id} \"{task.title}\" successfully deleted"}, 200)

@task_bp.route("/<task_id>/<complete_status>", methods=["PATCH"])
def mark_complete(task_id, complete_status):
    task = validate_id(Task, task_id)
    if complete_status == "mark_complete":
        task.completed_at = datetime.now()
    elif complete_status == "mark_incomplete":
        task.completed_at = None
    db.session.commit()
    return make_response({"task": task.to_dict()}, 200)
