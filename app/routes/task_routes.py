from flask import Blueprint, abort, make_response, request, Response
from ..models.task import Task
from ..db import db

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.post("")
def create_task():
    request_body = request.get_json()

    title = request_body["title"]
    description = request_body["description"]
    new_task = Task(title=title, description=description)

    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201

@tasks_bp.get("")
def get_all_tasks():
    tasks_query = db.select(Task).order_by(Task.id)
    tasks = db.session.scalars(tasks_query)
    
    return [task.to_dict() for task in tasks], 200

@tasks_bp.get("/<task_id>")
def get_saved_task_by_id(task_id):
    task = validate_task(task_id)
    return {"task": task.to_dict()}, 200

@tasks_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body.get("title", task.title)
    task.description = request_body.get("description", task.description)

    db.session.commit()

    return {"task": task.to_dict()}, 200

@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_task(task_id)
    
    db.session.delete(task)
    db.session.commit()

    return {"details": f"Task {task_id} \"{task.title}\" successfully deleted"}, 200
   
def validate_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        abort(make_response({"message": f"Task {task_id} incorrect value, expected integer"}, 400))

    task_query = db.select(Task).where(Task.id == task_id)
    task = db.session.scalar(task_query)

    if not task:
        abort(make_response({"message": f"Task {task_id} not found"}, 404))
    return task