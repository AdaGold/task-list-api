from flask import Blueprint, request, jsonify, make_response, abort
from app.models.task import Task
from app.models.goal import Goal
from app import db
from sqlalchemy import asc, desc
from datetime import datetime, timezone
import requests, os

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model

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
    task = validate_model(Task, id)

    return jsonify({"task":task.to_dict()}), 200


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        abort(make_response({"details": "Invalid data"}, 400))

    new_task = Task.from_dict(request_body)
    
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task":new_task.to_dict()}), 201


@tasks_bp.route("/<id>", methods=["PUT"])
def update_task(id):
    # TODO: Handle possible keyerrors like in post
    task = validate_model(Task, id)
    request_body=request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return jsonify({"task":task.to_dict()}), 200


@tasks_bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    task = validate_model(Task, id)

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
    task = validate_model(Task, id)

    task.completed_at = datetime.now(timezone.utc)
    db.session.commit()

    post_message_to_slack(task)

    return jsonify({"task":task.to_dict()}), 200


@tasks_bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(id):
    task = validate_model(Task, id)

    task.completed_at = None
    db.session.commit()

    return jsonify({"task":task.to_dict()}), 200

########## Wave 4 ###########
@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        abort(make_response({"details": "Invalid data"}, 400))

    new_goal = Goal.from_dict(request_body)

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
    goal = validate_model(Goal, id)

    return jsonify({"goal": goal.to_dict()}), 200

@goals_bp.route("<id>", methods=["PUT"])
def update_goal(id):
    # TODO: Handle possible keyerrors like in post
    pass

@goals_bp.route("<goal_id>/tasks", methods=["POST"])
def create_task(goal_id):
    request_body = request.get_json()

    new_task = Task.from_dict(request_body)
    
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"id":goal_id}), 200






