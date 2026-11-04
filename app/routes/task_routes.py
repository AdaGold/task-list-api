from flask import Blueprint
from app.models.task import Task
from app.db import db

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

@task_bp.get("")
def get_all_tasks():
    query = db.select(Task).order_by(Task.id)
    tasks = db.session.scalars(query)

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    return tasks_response