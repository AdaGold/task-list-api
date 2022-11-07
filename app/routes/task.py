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
    
    return {cls.__name__: model.to_dict()}

# CREATE
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    created_task = {"task": new_task.to_dict()}
    return make_response(created_task, 201)

# READ
@tasks_bp.route("", methods=["GET"])
def handle_tasks():
    tasks = Task.query.all()
    tasks_response = [task.to_dict() for task in tasks]

    return jsonify(tasks_response), 200

@tasks_bp.route("/<task_id>", methods=["GET"])
def handle_one_task(task_id):
    task = validate_model(Task, task_id)
    return jsonify(task), 200

# UPDATE

# DELETE