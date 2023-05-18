import os
from app import db
import requests
from datetime import date
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, make_response, request

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')
goals_bp = Blueprint('goals', __name__, url_prefix='/goals')

SLACK_API_URL = "https://slack.com/api/chat.postMessage"
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")

# Get all tasks
@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    sort_method = request.args.get('sort')

    if not sort_method:
        tasks = Task.query.all()
    elif sort_method == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort_method == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_json())

    return jsonify(tasks_response)

# Create a task
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if not "title" in request_body or not "description" in request_body:  # or \
        # not "completed_at" in request_body:
        return jsonify({
            "details": "Invalid data"
        }), 400

    new_task = Task(title=request_body["title"],
                    description=request_body["description"])
    
    if "completed_at" in request_body:
        new_task.completed_at = request_body["completed_at"]

    db.session.add(new_task)
    db.session.commit()

    return {
        "task": new_task.to_json()
    }, 201

# Get one task
@tasks_bp.route("/<task_id>", methods=["GET"])
def read_single_task(task_id):
    task = Task.query.get(task_id)

    if task:
        return {
            "task": task.to_json()
        }
    else:
        return {"message": f"Task {task_id} not found"}, 404

# Update a task
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return {"message": f"Task {task_id} not found"}, 404

    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]
    # if request_body["completed_at"]:
    #     task.completed_at = datetime.utcnow

    db.session.add(task)
    db.session.commit()

    return {
        "task": task.to_json()
    }, 200

# Delete a task
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return {"message": f"Task {task_id} not found"}, 404

    db.session.delete(task)
    db.session.commit()

    return {
        "details": f"Task {task_id} \"{task.title}\" successfully deleted"
    }, 200

# Mark a task complete
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    task = Task.query.get(task_id)
    
    if not task:
        return {"message": f"Task {task_id} not found"}, 404

    task.completed_at = date.today()

    db.session.add(task)
    db.session.commit()
    
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
    }
    
    if task.completed_at:
        data = {
            "channel": "task-notifications",
            "text": f"Someone just completed the task {task.title}!",
        }
    else:
        data = {
            "channel": "task-notifications",
            "text": f"Task {task.title} has been marked incomplete",
        }

    r = requests.post(SLACK_API_URL, headers=headers, data=data)

    return {
        "task": task.to_json()
    }, 200


# Mark a task incomplete
@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    task = Task.query.get(task_id)
    
    if not task:
        return {"message": f"Task {task_id} not found"}, 404

    task.completed_at = None

    db.session.add(task)
    db.session.commit()

    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
    }
    
    return {
        "task": task.to_json()
    }, 200

# Get all goals
@goals_bp.route("", methods=["GET"])
def read_all_goals():
    goals = Goal.query.all()
    goals_json = []

    for goal in goals:
        goals_json.append(goal.to_json())

    return jsonify(goals_json)

# Get one goal
@goals_bp.route("/<goal_id>", methods=["GET"])
def read_single_goal(goal_id):
    goal = Goal.query.get(goal_id)

    if goal:
        return {
            "goal": goal.to_json()
        }
    else:
        return {"message": f"Goal {goal_id} not found"}, 404

# Create a goal
@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    if not "title" in request_body:
        return jsonify({
            "details": "Invalid data"
        }), 400

    new_goal = Goal(title=request_body["title"])

    db.session.add(new_goal)
    db.session.commit()

    return {
        "goal": new_goal.to_json()
    }, 201

# Update a goal
@ goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if not goal:
        return {"message": f"Goal {goal_id} not found"}, 404

    request_body = request.get_json()
    goal.title = request_body["title"]

    db.session.add(goal)
    db.session.commit()

    return {
        "goal": goal.to_json()
    }, 200

# Delete a goal
@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if not goal:
        return {"message": f"Goal {goal_id} not found"}, 404

    db.session.delete(goal)
    db.session.commit()

    return {
        "details": f"Goal {goal_id} \"{goal.title}\" successfully deleted"
    }, 200

# Get all tasks for a goal
@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def goal_tasks(goal_id):
    goal = Goal.query.get(goal_id)

    if not goal:
        return {"message": f"Goal {goal_id} not found"}, 404

    answer = {
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": [],
    }

    for task in goal.tasks:
        answer["tasks"].append(task.to_json())

    return answer, 200

# Add a task to a goal
@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def goal_tasks_post(goal_id):
    goal = Goal.query.get(goal_id)

    if not goal:
        return {"message": f"Goal {goal_id} not found"}, 404

    request_body = request.get_json()

    answer = {
        "id": goal.goal_id,
        "task_ids": request_body["task_ids"],
    }

    for task_id in request_body["task_ids"]:
        task = Task.query.get(task_id)
        if not task:
            return {
                "message": 
                    f"Task {task_id} not found"
            }, 404

        goal.tasks.append(task)

    db.session.commit()

    return answer, 200