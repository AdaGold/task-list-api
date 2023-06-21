from flask import Blueprint, jsonify, request, make_response, abort
from app.models.task import Task
from app.models.goal import Goal
from app import db
import datetime as dt
import os
import requests

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

def validate_item(model, item_id):
    try:
        item_id = int(item_id)
    except:
        abort(make_response({"message": "Invalid id"}), 400)

    item = model.query.get(item_id)

    if not item:
        abort(make_response({"message": f"Id {item_id} not found."}, 404))

    return item

@tasks_bp.route("", methods=["GET"])
def read_all_tasks():

    sort_query = request.args.get("sort")
    if sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    elif sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    else:
        tasks = Task.query.all()

    tasks_response = []

    for task in tasks:
        tasks_response.append(task.to_dict())
    return jsonify(tasks_response), 200

@tasks_bp.route("", methods=["POST"])
def add_one_task():
    request_body = request.get_json()

    try:
        new_task = Task(
            title=request_body["title"],
            description=request_body["description"],
            )
    except KeyError:
        return make_response({"details": "Invalid data"}), 400

    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201
    # return make_response(jsonify(f"task {new_task.title} successfully created"), 201)


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task_by_id(task_id):
    # validate task id
    task = validate_item(Task, task_id)

    return {"task": task.to_dict()}

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    task = validate_item(Task, task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {"task": task.to_dict()}, 200

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH", "POST"])
def mark_one_task_complete(task_id):
    task = validate_item(Task, task_id)

    task.is_complete = True
    task.completed_at = dt.datetime.now()

    slack_token = os.environ.get("SLACK_TOKEN")
    header = {"Authorization": f"Bearer {slack_token}"}
    channel = os.environ.get("CHANNEL_ID")

    response = requests.post("https://slack.com/api/chat.postMessage", headers=header, 
        data={
        "channel": channel,
        "text": f"Someone just completed the task {task.title}"
    })

    db.session.commit()

    if response.status_code == 200:
        return make_response({"task": task.to_dict()}), 200
    else:
        return "Error", 404

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_one_task_incomplete(task_id):
    task = validate_item(Task, task_id)

    task.is_complete = False
    task.completed_at = None

    db.session.commit()

    return make_response({"task": task.to_dict()}), 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task = validate_item(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f'Task {task_id} "{task.title}" successfully deleted'})


## Goal Routes ##

@goals_bp.route("", methods=["POST"])
def add_one_goal():
    request_body = request.get_json()

    try:
        new_goal = Goal(
            title=request_body["title"]
            )
    except KeyError:
        return make_response({"details": "Invalid data"}), 400

    db.session.add(new_goal)
    db.session.commit()

    return make_response({"goal": new_goal.to_dict()}, 201)


@goals_bp.route("", methods=["GET"])
def get_all_goals():

    goals = Goal.query.all()

    goal_list = []

    for goal in goals:
        goal_list.append(goal.to_dict())

    return jsonify(goal_list)

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal_by_id(goal_id):
    goal = validate_item(Goal, goal_id)

    return make_response({"goal": goal.to_dict()}, 200)

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_one_goal(goal_id):
    goal = validate_item(Goal, goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return make_response({"goal": goal.to_dict()}, 200)

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_goal(goal_id):
    goal = validate_item(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response({
        "details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'
    }, 200)

## wave 6 combo routes ##

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_tasks_to_goal(goal_id):
    goal = validate_item(Goal, goal_id)

    request_body = request.get_json()

    for task_id in request_body["task_ids"]:
        task = validate_item(Task, task_id)
        task.goal_id = goal_id

    db.session.commit()

    task_ids = [task.task_id for task in goal.tasks]

    return {"id": goal.goal_id, "task_ids": task_ids}, 200

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_all_tasks_for_one_goal(goal_id):
    goal = validate_item(Goal, goal_id)

    goal_dict = goal.to_dict()

    if not goal.tasks:
        goal_dict["tasks"] = []

    return goal_dict, 200
    