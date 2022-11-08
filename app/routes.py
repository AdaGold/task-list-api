from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model

    
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    
    if not all(["title" in request_body, "description" in request_body]):#, "completed_at" in request_body ]):
        return {"details" : "Invalid data"}, 400

    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201


@tasks_bp.route("", methods=["GET"])
def get_tasks():

    title_query = request.args.get("title")
    if title_query:
        tasks = Task.query.filter_by(title=title_query)
    else:
        tasks = Task.query.all()

    task_response = []
    for task in tasks:
        task_response.append(task.to_dict())
    return jsonify(task_response)


@tasks_bp.route("/<id>", methods=["GET"])
def get_task(id):
    task = validate_model(Task, id)
    return {"task": task.to_dict()}, 200
