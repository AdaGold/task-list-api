from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import request, Blueprint, jsonify # make_response,
from sqlalchemy import asc, desc
from datetime import datetime
import os
from slack_sdk import WebClient
import requests

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@tasks_bp.route("", methods = ["POST"])
def add_task():
    """Adds new task to the Task table"""
    response_body = request.get_json()
    if len(response_body) != 3:
        return jsonify({"details": f"Invalid data"}), 400
    task = Task(
        title = response_body["title"],
        description = response_body["description"],
        completed_at = response_body["completed_at"]
        )  
    db.session.add(task)
    db.session.commit()
    return jsonify({"task": task.to_dict()}), 201

@tasks_bp.route("/<task_id>", methods=["GET"]) 
def get_one_task(task_id):
    """Gets data of a particular task"""
    task = Task.query.get(task_id)
    if not task:
        return jsonify(None), 404
    return jsonify({"task": task.to_dict()}), 200  

@tasks_bp.route("", methods=["GET"])
def get_tasks():
    """
    Returns an array of tasks.
    - No arg provided -> return all tasks
    - Arg provided -> return tasks sorted by title
    """
    task_order = request.args.get("sort")
    if task_order == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif task_order == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
    response_body = [] 
    for task in tasks:
        response_body.append(task.to_dict())
    return jsonify(response_body), 200

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    """Updates a portion of a single task"""
    task = Task.query.get(task_id)
    if not task:
        return jsonify(None), 404
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body["completed_at"]
    db.session.commit()
    return jsonify({"task": task.to_dict()}), 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    """Deletes one task from the Task table"""
    task = Task.query.get(task_id)
    if not task:
        return jsonify(None), 404
    db.session.delete(task)
    db.session.commit()
    return ({"details": f"Task {task_id} \"{task.title}\" successfully deleted"}, 200)

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    """Marks Task complete"""
    task = Task.query.get(task_id) 
    if not task:
        return jsonify(None), 404
    if not task.is_complete(): 
        task.completed_at = datetime.now()
        db.session.add(task)
        db.session.commit()
        send_slack_task_notification(task)
    return jsonify({"task": task.to_dict()}), 200

def send_slack_task_notification(task):
    """Posts message to a Slack channel"""
    """
    slack_token = os.environ.get("SLACK_BOT_TOKEN")
    client = WebClient(token=slack_token)
    channel_id = "C0215S41XGS"
    client.chat_postMessage(
        channel=channel_id,
        text=(f"Someone just completed the task {task.title}")
        )
    """
    SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
    notification = f"Someone just completed the task {task.title}"
    url = f"https://slack.com/api/chat.postMessage?channel=task-notifications&text={notification}"
    headers = {Authorization': f'Bearer {SLACK_BOT_TOKEN}'}
    return requests.request("POST", url, headers=headers)

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    """Marks Task complete"""
    task = Task.query.get(task_id) 
    if not task:
        return jsonify(None), 404
    if task.is_complete(): 
        task.completed_at = None
        db.session.add(task)
        db.session.commit()
    return jsonify({"task": task.to_dict()}), 200

@goals_bp.route("", methods = ["POST"])
def add_goal():
    """Adds a new goal to the Goal table"""
    response_body = request.get_json()
    if "title" not in response_body:
        return jsonify({"details": "Invalid data"}), 400
    goal = Goal(title = response_body["title"])  
    db.session.add(goal)
    db.session.commit()
    return jsonify({"goal": goal.to_dict()}), 201

@goals_bp.route("", methods=["GET"])
def get_goals():
    """Returns an array of goals."""
    goals = Goal.query.all()
    response_body = [] 
    for goal in goals:
        response_body.append(goal.to_dict())
    return jsonify(response_body), 200

@goals_bp.route("/<goal_id>", methods=["GET"]) 
def get_goal(goal_id):
    """Gets data of a particular goal"""
    goal = Goal.query.get(goal_id)
    if not goal:
        return jsonify(None), 404
    return jsonify({"goal": goal.to_dict()}), 200  

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    """Updates a portion of a single goal"""
    goal = Goal.query.get(goal_id)
    if not goal:
        return jsonify(None), 404
    request_body = request.get_json()
    goal.title = request_body["title"]
    db.session.commit()
    return jsonify({"goal": goal.to_dict()}), 200

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    """Deletes one goal from the goal table"""
    goal = Goal.query.get(goal_id)
    if not goal:
        return jsonify(None), 404
    db.session.delete(goal)
    db.session.commit()
    return ({"details": f"Goal {goal_id} \"{goal.title}\" successfully deleted"}, 200)
