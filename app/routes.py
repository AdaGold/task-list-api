from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task
import os, requests


task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# ================================
# Create One Task 
# ================================
@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task.from_json(request_body)

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": new_task.to_json()}), 201