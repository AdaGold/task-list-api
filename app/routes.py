from flask import Blueprint, request, jsonify, make_response, abort
from app.models.task import Task
from app.models.goal import Goal
from app import db
from sqlalchemy import asc, desc
from datetime import datetime, timezone
import requests, os

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

def validate_task(task_id):
    #TODO: refactor so that the parameter accepts the class
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message":f"Task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message":f"Task {task_id} not found"}, 404))

    return task

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    sort_query = request.args.get("sort")
    tasks_query = Task.query

    if sort_query == "asc":
        tasks_query = Task.query.order_by(asc("title"))
    if sort_query == "desc":
        tasks_query = Task.query.order_by(desc("title"))

    tasks = tasks_query.all()
    tasks_response = [task.to_dict() for task in tasks]
    
    return jsonify(tasks_response), 200


@tasks_bp.route("/<id>", methods=["GET"])
def get_one_task(id):
    task = validate_task(id)

    return jsonify({"task":task.to_dict()}), 200


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        abort(make_response({"details": "Invalid data"}, 400))

    # TODO: Refactor with from_dict
    new_task = Task(title=request_body["title"],
                    description=request_body["description"])
    
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task":new_task.to_dict()}), 201


@tasks_bp.route("/<id>", methods=["PUT"])
def update_task(id):
    # TODO: Handle possible keyerrors like in post
    task = validate_task(id)
    request_body=request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return jsonify({"task":task.to_dict()}), 200


@tasks_bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    task = validate_task(id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({"details": f'Task {id} "{task.title}" successfully deleted'}), 200


########## Wave 3 ###########
def post_message_to_slack(task):
    SLACK_API_ROOT = "https://slack.com/api/chat.postMessage"
    CHANNEL_ID = os.environ.get("CHANNEL_ID")

    message = f"Someone just completed the task {task.title}"
    endpoint_url = SLACK_API_ROOT + "?channel=" + CHANNEL_ID + "&text=" + message

    response = requests.post(endpoint_url, headers={"Authorization": os.environ.get("SLACK_BOT_TOKEN")})

    # TODO: Create a tailored error message
    # raises an error if status code is not 200
    response.raise_for_status()

    return response

@tasks_bp.route("/<id>/mark_complete", methods=["PATCH"])
def mark_task_complete(id):
    task = validate_task(id)

    task.completed_at = datetime.now(timezone.utc)
    db.session.commit()

    post_message_to_slack(task)

    return jsonify({"task":task.to_dict()}), 200


@tasks_bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(id):
    task = validate_task(id)

    task.completed_at = None
    db.session.commit()

    return jsonify({"task":task.to_dict()}), 200

########## Wave 4 ###########
def validate_goal(goal_id):
    # TODO: refactor so that parameter accepts class
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"message": f"Goal {goal_id} invalid"}, 400))
    
    goal = Goal.query.get(goal_id)

    if not goal:
        abort(make_response({"message": f"Goal {goal_id} not found"}, 404))

    return goal 

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        abort(make_response({"details": "Invalid data"}, 400))

    new_goal = Goal(title=request_body["title"])

    db.session.add(new_goal)
    db.session.commit()

    return jsonify({"goal":new_goal.to_dict()}), 201

@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()
    goals_response = [goal.to_dict() for goal in goals]

    return jsonify(goals_response), 200

@goals_bp.route("/<id>", methods=["GET"])
def get_one_goal(id):
    goal = validate_goal(id)

    return jsonify({"goal": goal.to_dict()}), 200

@goals_bp.route("<id>", methods=["PUT"])
def update_goal(id):
    # TODO: Handle possible keyerrors like in post
    pass





