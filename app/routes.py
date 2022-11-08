from flask import Blueprint, request, jsonify, make_response, abort
from app.models.task import Task
from app import db

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message":f"Task #{task_id} invalid"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message":f"Task #{task_id} not found"}, 404))

    return task

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks = Task.query.all()
    tasks_response = [task.to_dict() for task in tasks]
    
    return jsonify(tasks_response), 200

@tasks_bp.route("", methods=["POST"])
def create_one_task():
    request_body = request.get_json()
    if ("title" not in request_body or "description" not in request_body):
        abort(make_response({"details": "Invalid data"}, 400))

    new_task = Task(title=request_body["title"],
                    description=request_body["description"])
                    #is_complete=request_body["completed_at"])
    
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task":new_task.to_dict()}), 201

@tasks_bp.route("/<id>", methods=["GET"])
def get_one_task(id):
    task = validate_task(id)

    return jsonify({"task":task.to_dict()}), 200

#@tasks_bp.route("/<id>", methods=["DELETE"])
