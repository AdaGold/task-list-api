from flask import Blueprint, request, jsonify, make_response, abort
from app.models.task import Task
from app import db

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks = Task.query.all()
    tasks_response = []

    for task in tasks:
        tasks_response.append({'id':task['id'],
        'name':task['name'],
        'description': task['description'],
        'completed_at': task['completed_at']})
    
    return jsonify(tasks_response), 200

