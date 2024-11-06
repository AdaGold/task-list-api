from flask import Blueprint, request
from sqlalchemy import desc
from datetime import datetime
from app.routes.route_utilities import create_model, validate_model
from app.models.task import Task
from app.db import db

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.post("")
def create_task():
    request_body = request.get_json()
    return create_model(Task, request_body)

@tasks_bp.get("")
def get_all_tasks():
    sort_param = request.args.get("sort")
    query = db.select(Task)
    
    if sort_param:
        if sort_param == "desc":
            query = query.order_by(desc(Task.title))
        else:
            query = query.order_by(Task.title)

    tasks = db.session.scalars(query)
    
    return [task.to_dict() for task in tasks], 200

@tasks_bp.get("/<task_id>")
def get_saved_task_by_id(task_id):
    task = validate_model(Task, task_id)

    return {"task": task.to_dict()}, 200

@tasks_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body.get("title", task.title)
    task.description = request_body.get("description", task.description)

    db.session.commit()

    return {"task": task.to_dict()}, 200

@tasks_bp.patch("/<task_id>/mark_complete")
def update_task_as_complete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = datetime.now()

    db.session.commit()

    # make call to Slack API, post message to workspace and channel
    return {"task": task.to_dict()}, 200

@tasks_bp.patch("/<task_id>/mark_incomplete")
def update_task_as_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None

    db.session.commit()

    return {"task": task.to_dict()}, 200

@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)
    
    db.session.delete(task)
    db.session.commit()

    return {"details": f"Task {task_id} \"{task.title}\" successfully deleted"}, 200