from flask import Blueprint, jsonify, make_response, abort, request
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"details":"Invalid data"}, 400))

    task = cls.query.get(model_id)

    if not task:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return task

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    try:
        new_task = Task.from_dict(request_body)
    except KeyError:
        return jsonify({'details': 'Invalid data'}), 400

    db.session.add(new_task)
    db.session.commit()

    return jsonify({'task': new_task.to_dict()}), 201

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    
    request_body = request.get_json()
    
    task.title = request_body["title"]
    task.description = request_body["description"]
    
    db.session.commit()
    return jsonify({'task': task.to_dict()}), 200


@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id)
    return jsonify({'task': task.to_dict()}), 200

@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    task_query = request.args.get("task")
    if task_query:
        tasks = Task.query.filter_by(task=task_query)
    else:
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    return jsonify(tasks_response), 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)
    
    db.session.delete(task)
    db.session.commit()
    
    return jsonify({"details": f'Task {task.task_id} "{task.title}" successfully deleted'})
