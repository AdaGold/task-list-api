from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
from .routes_helper import error_message

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def validate_task(id):
    try:
        id = int(id)
    except:
        abort(make_response({"message":f"task {task.id} invalid"}, 400))
    
    task = Task.query.get(id)

    if not task:
        abort(make_response({"message":f"task {id} not found"}, 404))

    return task

def make_task_safely(data_dict):
    try:
        return Task.from_dict(data_dict)
    except KeyError as err:
        error_message(f"Missing key: {err}", 400)


@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    
    tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.is_complete,
                # "completed_at": task.completed_at
            }
        )
    return jsonify(tasks_response), 200

def get_task_record_by_id(id):
    try:
        id = int(id)
    except ValueError:
        error_message(f"Invalid id {id}", 400)

    task = Task.query.get(id)

    if task:
        return task
    
    error_message(f"No task with id {id} found", 404)

@tasks_bp.route("/<id>", methods=("GET",))
def read_task_by_id(id):
    task = get_task_record_by_id(id)
    return jsonify({"task":{
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "is_complete": task.is_complete
    }}), 200

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    
    new_task = make_task_safely(request_body)

    db.session.add(new_task)
    db.session.commit()

    response = {"task":{
        "id":new_task.id,
        "title":new_task.title,
        "description":new_task.description,
        "is_complete":new_task.is_complete
    }}

    return make_response(jsonify(response), 201)

@tasks_bp.route("/<id>", methods=["PUT"])
def update_task(id):
    task = validate_task(id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    response = {"task":{
        "id":task.id,
        "title":task.title,
        "description":task.description,
        "is_complete":task.is_complete
    }}

    return make_response(jsonify(response), 200)