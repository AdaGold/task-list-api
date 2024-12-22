from flask import Blueprint, request
from sqlalchemy import desc
from datetime import datetime
from app.routes.route_utilities import create_model, validate_model, send_slack_message
from app.models.task import Task
from app.db import db


bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@bp.post("")
def create_task():
    response = create_model(Task, request.get_json())
    return {"task": response}, 201


@bp.get("")
def get_tasks():
    sort_param = request.args.get("sort")
    query = db.select(Task)

    sort_method = request.args.get('sort')

    if sort_method and sort_method == "asc":
        query = query.order_by(Task.id.asc())
    if sort_method and sort_method == "desc":
        query = query.order_by(Task.id.desc())

    tasks = db.session.scalars(query)
    
    return [task.to_dict() for task in tasks]


@bp.get("/<task_id>")
def get_task_by_id(task_id):
    task = validate_model(Task, task_id)
    return {"task": task.to_dict()}


@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body.get("title", task.title)
    task.description = request_body.get("description", task.description)

    db.session.commit()

    return {"task": task.to_dict()}


@bp.patch("/<task_id>/mark_complete")
def update_task_as_complete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = datetime.now()
    db.session.commit()

    send_slack_message(task.title)

    return {"task": task.to_dict()}


@bp.patch("/<task_id>/mark_incomplete")
def update_task_as_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None
    db.session.commit()

    return {"task": task.to_dict()}


@bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)
    
    db.session.delete(task)
    db.session.commit()

    return {"details": f"Task {task_id} \"{task.title}\" successfully deleted"}
