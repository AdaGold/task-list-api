from app import db
from app.models.task import Task
from flask import Blueprint, request, jsonify

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["GET"])
def tasks():
    tasks = Task.query.all()
    response = [task.to_dict() for task in tasks]
    return jsonify(response), 200
