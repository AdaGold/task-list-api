from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task
import os, requests


task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# ================================
# Create one task 
# TODO: handle cases with missing titles/completed_at/description
# ================================
@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    try:
        new_task = Task.create(request_body)
    except KeyError as error:
        return make_response({"details": "Invalid data"}, 400)



    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": new_task.to_json()}), 201

# ==================================
# Get all tasks  
# ==================================
@task_bp.route("", methods=["GET"])
def get_all_tasks():
    results_list = []
    all_tasks = Task.query.all()
    for task in all_tasks:
        results_list.append(task.to_json())
    return jsonify(results_list), 200

# ==================================
# Get one task by id number
# ==================================
@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    return jsonify({"task": validate_id(Task, task_id).to_json()}), 200

# ==================================
# Update one task 
# TODO: fix tests for this 
# ==================================
@task_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    request_body = request.get_json()
    task = validate_id(Task, task_id)
    task.update(request_body)

    db.session.commit()
    return jsonify({"task": task.to_json()}), 200

# ==================================
# Delete one task by id
# ==================================
@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task = validate_id(Task, task_id)
    db.session.delete(task)
    db.session.commit()
    return make_response({"details":f'Task {task.task_id} "{task.title}" successfully deleted'}, 200)

# ==================================
# Helper function to validate id
# ==================================
def validate_id(class_name,id):
    try:
        id = int(id)
    except:
        abort(make_response({"message":f"Id {id} is an invalid id"}, 400))

    query_result = class_name.query.get(id)
    if not query_result:
        abort(make_response({"message":f"Id {id} not found"}, 404))

    return query_result