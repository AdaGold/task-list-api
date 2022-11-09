from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort

tasks_bp = Blueprint("task", __name__, url_prefix="/tasks")

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
    tasks = Task.query.all()
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

# DELETE
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)
    response_body = f"Task {task_id} \"{task.title}\" successfully deleted"

    db.session.delete(task)
    db.session.commit()
    
    return make_response({"details": response_body}, 200)