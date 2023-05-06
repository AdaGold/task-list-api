from flask import Blueprint, jsonify, make_response, request, abort
import requests
from app import db
from app.models.task import Task
from app.models.goal import Goal
from datetime import datetime
import os
from sqlalchemy.orm import lazyload
import json

def validate_item(cls, request_body):
    try:
        new_task = cls.from_dict(request_body)
    except KeyError:
        return abort(make_response({"details": "Invalid data"}, 400))
    return new_task

def validate_id(cls, id):
    try:
        id = int(id)
    except:
        return abort(make_response({"message": f"{cls.__name__} {id} invalid"}, 400))
    record = cls.query.get_or_404(id)
    return record

task_bp = Blueprint("task", __name__, url_prefix="/tasks")
@task_bp.route("", methods=["POST"])
def create_one_task():
    request_body = request.get_json()
    new_task = validate_item(Task, request_body)

    db.session.add(new_task)
    db.session.commit()

    return make_response({"task": new_task.to_dict()}, 201)

@task_bp.route("", methods=["GET"])
def get_all_tasks():
    response = []
    sort_query = request.args.get("sort")

    if sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    elif sort_query == "asc":
        tasks = Task.query.order_by(Task.title)
    else:
        tasks = Task.query.all()
    
    for task in tasks:
        response.append(task.to_dict())

    return jsonify(response), 200

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_id(Task, task_id)
    return make_response({"task": task.to_dict()}, 200)

@task_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    task = validate_id(Task, task_id)
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()
    return make_response({"task": task.to_dict()}, 200)

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task = validate_id(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f"Task {task.id} \"{task.title}\" successfully deleted"}, 200)

@task_bp.route("/<task_id>/<complete_status>", methods=["PATCH"])
def mark_complete(task_id, complete_status):
    task = validate_id(Task, task_id)
    if complete_status == "mark_complete":
        task.completed_at = datetime.now()
        requests.post("https://slack.com/api/chat.postMessage", json={"channel": "task-notifications", "text": f"Someone just completed the task {task.title}"}, headers={"Authorization": os.environ.get("SLACK_BOT_TOKEN")})
    elif complete_status == "mark_incomplete":
        task.completed_at = None
    db.session.commit()
    return make_response({"task": task.to_dict()}, 200)

goal_bp = Blueprint("goal", __name__, url_prefix="/goals")
@goal_bp.route("", methods=["POST"])
def create_one_goal():
    request_body = request.get_json()
    new_goal = validate_item(Goal, request_body)

    db.session.add(new_goal)
    db.session.commit()

    return make_response({"goal": new_goal.to_dict()}, 201)

@goal_bp.route("", methods=["GET"])
def get_all_goals():
    response = []
    goals = Goal.query.all()

    for goal in goals:
        response.append(goal.to_dict())
    return jsonify(response), 200

@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_id(Goal, goal_id)
    return make_response({"goal": goal.to_dict()}, 200)

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_one_goal(goal_id):
    goal = validate_id(Goal, goal_id)
    request_body = request.get_json()
    goal.title = request_body["title"]

    db.session.commit()
    return make_response({"goal": goal.to_dict()}, 200)

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_goal(goal_id):
    goal = validate_id(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()
    return make_response({"details": f"Goal {goal.id} \"{goal.title}\" successfully deleted"}, 200)

@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_tasks_to_goal(goal_id):
    goal = validate_id(Goal, goal_id)
    request_body = request.get_json()
    task_ids = request_body["task_ids"]
    for id in task_ids:
        goal.tasks.append(Task.query.get(id))
    db.session.commit()
    return jsonify(id=goal.id, task_ids=task_ids), 200

@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_of_one_goal(goal_id):
    goal = validate_id(Goal, goal_id)
    tasks = goal.tasks
    tasks_to_dict = []
    for task in tasks:
        tasks_to_dict.append(task.to_dict())
    return jsonify(id=goal.id, title=goal.title, tasks=tasks_to_dict), 200

