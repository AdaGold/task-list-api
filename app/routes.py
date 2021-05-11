from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import request, Blueprint, jsonify
from datetime import datetime
import os
# from slack_sdk import WebClient
from requests import post

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

def get_task_response(task, code=200):
    return jsonify({"task": task.to_dict()}), code

def get_goal_response(goal, code=200):
    return jsonify({"goal": goal.to_dict()}), code

def get_client_error_response():
    return jsonify(None), 404

####################### TASK ROUTES #######################

@tasks_bp.route("", methods = ["POST"])
def add_task():
    """Adds new task to the Task table"""
    request_body = request.get_json()
    if len(request_body) != 3:
        return jsonify({"details": f"Invalid data"}), 400
    task = Task(
        title = request_body["title"],
        description = request_body["description"],
        completed_at = request_body["completed_at"]
        )  
    db.session.add(task)
    db.session.commit()
    return get_task_response(task, code=201)

@tasks_bp.route("/<task_id>", methods=["GET"]) 
def get_one_task(task_id):
    """Gets data of a particular task"""
    task = Task.query.get(task_id)
    if not task:
        return get_client_error_response()
    return get_task_response(task) 

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
        return get_client_error_response()
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body["completed_at"]
    db.session.commit()
    return get_task_response(task)

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    """Deletes one task from the Task table"""
    task = Task.query.get(task_id)
    if not task:
        return get_client_error_response()
    db.session.delete(task)
    db.session.commit()
    return ({"details": f"Task {task_id} \"{task.title}\" successfully deleted"}, 200)

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    """Marks Task complete"""
    task = Task.query.get(task_id) 
    if not task:
        return get_client_error_response()
    if not task.is_complete(): 
        task.completed_at = datetime.now()
        db.session.commit()
        send_slack_task_notification(task)
    return get_task_response(task)

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
    headers = {"Authorization": f"Bearer {SLACK_BOT_TOKEN}"}
    return post(url, headers=headers)

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    """Marks Task complete"""
    task = Task.query.get(task_id) 
    if not task:
        return get_client_error_response()
    if task.is_complete(): 
        task.completed_at = None
        db.session.commit()
    return get_task_response(task)

####################### GOAL ROUTES #######################

@goals_bp.route("", methods = ["POST"])
def add_goal():
    """Adds a new goal to the Goal table"""
    request_body = request.get_json() 
    if "title" not in request_body:
        return jsonify({"details": "Invalid data"}), 400
    goal = Goal(title = request_body["title"])  
    db.session.add(goal)
    db.session.commit()
    return get_goal_response(goal, code=201)

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
        return get_client_error_response()
    return get_goal_response(goal)

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    """Updates a portion of a single goal"""
    goal = Goal.query.get(goal_id)
    if not goal:
        return get_client_error_response()
    request_body = request.get_json()
    goal.title = request_body["title"]
    db.session.commit()
    return get_goal_response(goal)

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    """Deletes one goal from the goal table"""
    goal = Goal.query.get(goal_id)
    if not goal:
        return get_client_error_response()
    db.session.delete(goal)
    db.session.commit()
    return ({"details": f"Goal {goal_id} \"{goal.title}\" successfully deleted"}, 200)

@goals_bp.route("<goal_id>/tasks", methods=["POST"])
def add_tasks_to_goal(goal_id):
    """Adds List of Task IDs to a Goal"""
    goal = Goal.query.get(goal_id)
    if not goal:
        return get_client_error_response()
    request_body = request.get_json()
    for task_id in request_body["task_ids"]:
        task = Task.query.get(task_id)
        task.goal_id = goal.goal_id
    return jsonify({
        "id": goal.goal_id,
        "task_ids": request_body["task_ids"]
        }), 200

@goals_bp.route("<goal_id>/tasks", methods=["GET"])
def get_tasks_of_goal(goal_id):
    """Gets Tasks of One Goal"""
    goal = Goal.query.get(goal_id)
    if not goal:
        return get_client_error_response()
    tasks = Task.query.filter_by(goal_id=goal.goal_id)
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    return jsonify({
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": tasks_response
        }), 200