from flask import Blueprint, jsonify, request, make_response, abort
from app.models.task import Task
from app import db

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message": "Invalid task id"}), 400)

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message": "Task id {task_id} not found."}, 404))

    return task

@tasks_bp.route("", methods=["GET"])
def read_all_tasks():

    sort_query = request.args.get("sort")
    if sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    elif sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    else:
        tasks = Task.query.all()
        
    tasks_response = []

    for task in tasks:
        tasks_response.append(task.to_dict())
    return jsonify(tasks_response), 200

@tasks_bp.route("", methods=["POST"])
def add_one_task():
    request_body = request.get_json()

    try:
        new_task = Task(
            title=request_body["title"],
            description=request_body["description"],
            )
    except KeyError:
        return make_response({"details": "Invalid data"}), 400

    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201
    # return make_response(jsonify(f"task {new_task.title} successfully created"), 201)


@tasks_bp.route("<task_id>", methods=["GET"])
def get_one_task_by_id(task_id):
    # validate task id
    task = validate_task(task_id)

    return {"task": task.to_dict()}

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {"task": task.to_dict()}, 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f'Task {task_id} "{task.title}" successfully deleted'})