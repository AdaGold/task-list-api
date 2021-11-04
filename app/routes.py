from datetime import datetime
from flask import Blueprint, jsonify, make_response, request
from app.models.task import Task
from app.models.goal import Goal
from app import db
from sqlalchemy import desc, asc
import requests
import os

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
        return jsonify({"details": "Invalid data"}), 400
    
    new_task = Task(title=request_body["title"], 
        description=request_body["description"],
        completed_at=request_body["completed_at"])

    db.session.add(new_task)
    db.session.commit()
    
    return jsonify({"task": new_task.task_dict()}), 201

@tasks_bp.route("", methods=["GET"])
def index():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks = Task.query.order_by(asc(Task.title)).all()
    elif sort_query =="desc":
        tasks = Task.query.order_by(desc(Task.title)).all()
    else:
        tasks = Task.query.all()
    
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.task_dict())

    return jsonify(tasks_response), 200   

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        return "", 404

    return jsonify({"task": task.task_dict()}), 200

@tasks_bp.route("/<task_id>", methods=["PUT"])
def put_task(task_id):
    task = Task.query.get(task_id)
    request_body = request.get_json()

    if not task:
        return "", 404

    if "title" not in request_body or "description" not in request_body:
        return jsonify({"details": "Invalid data"}), 400

    task.title =request_body["title"]
    task.description =request_body["description"]

    db.session.commit()

    return jsonify({"task": task.task_dict()}), 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return "", 404

    db.session.delete(task)
    db.session.commit()
    
    return jsonify({"details": f"Task {task_id} \"{task.title}\" successfully deleted"}), 200

def update_completion(task_id, value, send_message=False):
    task = Task.query.get(task_id)

    if not task:
        return "", 404

    task.completed_at = value

    db.session.commit()

    if send_message:
        api_key = os.environ.get("SLACK_API_KEY")
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        url = f"https://slack.com/api/chat.postMessage?channel=task-notifications&text=Someone just completed the task {task.title}"
        requests.post(url, headers=headers)

    return jsonify({"task": task.task_dict()}), 200

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    
    return update_completion(task_id, datetime.now(), send_message=True)


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):

    return update_completion(task_id, None)

#######################GGGGOOOOOOOOOOOOAAAAAAAAAAALLLLLLLL###############################################

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    
    if "title" not in request_body:
        return jsonify({"details": "Invalid data"}), 400
    
    new_goal = Goal(title=request_body["title"])

    db.session.add(new_goal)
    db.session.commit()

    return jsonify({"goal": new_goal.goal_dict()}), 201

@goals_bp.route("", methods=["GET"])
def index():
    goals = Goal.query.all()
    
    goals_response = []
    for goal in goals:
        goals_response.append(goal.goal_dict())

    return jsonify(goals_response), 200   

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_goal(goal_id):
    goal = Goal.query.get(goal_id)

    if not goal:
        return "", 404

    return jsonify({"goal": goal.goal_dict()}), 200

@goals_bp.route("/<goal_id>", methods=["PUT"])
def put_goal(goal_id):
    goal = Goal.query.get(goal_id)
    request_body = request.get_json()

    if not goal:
        return "", 404

    if "title" not in request_body:
        return jsonify({"details": "Invalid data"}), 400

    goal.title =request_body["title"]

    db.session.commit()

    return jsonify({"goal": goal.goal_dict()}), 200

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = Goal.query.get(goal_id)
    
    if not goal:
        return "", 404

    db.session.delete(goal)
    db.session.commit()
    
    return jsonify({"details": f"Goal {goal_id} \"{goal.title}\" successfully deleted"}), 200

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_task_to_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal is None:
        return "", 404

    request_body = request.get_json()
    if "task_ids" not in request_body:
        return jsonify({"details": "Invalid data"}), 400

    for task_id in request_body["task_ids"]:
        task = Task.query.get(task_id)
        task.goal = goal
        goal.tasks.append(task)
        
    db.session.commit()

    return jsonify({
        "id": goal.goal_id,
        "task_ids": request_body["task_ids"]
    }), 200


@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_for_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal is None:
        return "", 404

    tasks = []
    for task in goal.tasks:
        tasks.append(task.task_dict())

    return jsonify({
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": tasks
    }), 200