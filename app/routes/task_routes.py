from flask import Blueprint, abort, make_response, Response, request
from .route_utilities import validate_model, create_model, get_models_with_filters, post_slack_message
from app.db import db
from app.models.task import Task
from sqlalchemy import asc, desc
from datetime import datetime
import pytz


tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


@tasks_bp.get("")
def get_all_tasks():
    query = db.select(Task)

    title_param_key = request.args.get("sort")

    if title_param_key == "asc":
        query = query.order_by(asc(Task.title))
    elif title_param_key == "desc":
        query = query.order_by(desc(Task.title))

    title_param = request.args.get("title")
    if title_param:
        query = query.where(Task.title.ilike(f"%{title_param}%"))

    description_param = request.args.get("description")
    if description_param:
        query = query.where(Task.description.ilike(f"%{description_param}%"))

    query = query.order_by(Task.id)
    tasks = db.session.scalars(query)

    response_body = [task.to_dict() for task in tasks]

    return response_body


@tasks_bp.post("")
def create_task():
    request_body = request.get_json()

    if not "title" in request_body or not "description" in request_body:
        response_body = {"details": "Invalid data"}
        return make_response(response_body, 400)

    title = request_body["title"]
    description = request_body["description"]

    new_task = Task.from_dict(request_body)
    db.session.add(new_task)
    db.session.commit()

    response_body = {"task": new_task.to_dict()}

    return response_body, 201


@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    response_body = {"task": task.to_dict()}
    return response_body


@tasks_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()
    task.title = request_body.get("title", task.title)
    task.description = request_body.get("description", task.description)
    db.session.commit()

    response_body = {"task": task.to_dict()}

    return make_response(response_body, 200)


@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)  
    db.session.delete(task)
    db.session.commit()

    response_body = {
        "details": f'Task {task.id} "{task.title}" successfully deleted'
    }
    return make_response(response_body, 200)


@tasks_bp.patch("/<task_id>/mark_complete")
def update_mark_complete_task(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = datetime.now(pytz.UTC)

    db.session.commit()

    # post_slack_message(task)

    response_body = {"task": task.to_dict()}

    return make_response(response_body, 200)


@tasks_bp.patch("/<task_id>/mark_incomplete")
def update_mark_incomplete_task(task_id):
    task = validate_model(Task, task_id) 

    task.completed_at = None
    db.session.commit()

    response_body = {"task": task.to_dict()}
    return make_response(response_body, 200)