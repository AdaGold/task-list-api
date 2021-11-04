from app import db
from app.models.task import Task
from app.models.goal import Goal
import requests
from flask import Blueprint, jsonify, request
from sqlalchemy import asc, desc
from datetime import date
import os

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


@tasks_bp.route("", methods=["GET"])
def read_tasks():
    sort_query = request.args.get("sort")
    if sort_query:
        if sort_query == "asc":
            tasks = Task.query.order_by(Task.title)
        else:
            tasks = Task.query.order_by(desc(Task.title))
    else:
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())

    return jsonify(tasks_response)


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    try:
        new_task = Task(title=request_body["title"],
                        description=request_body["description"], completed_at=request_body["completed_at"])

        db.session.add(new_task)
        db.session.commit()

        response = {
            "task": new_task.to_dict()
        }
        return jsonify(response), 201
    except KeyError:
        return jsonify({"details": "Invalid data"}), 400


@tasks_bp.route("/<id>", methods=["GET"])
def get_one_task(id):
    task = Task.query.get(id)
    if task is None:
        return jsonify(None), 404

    return {
        "task": task.to_dict()
    }


@tasks_bp.route("/<id>", methods=["PUT"])
def update_one_task(id):
    task = Task.query.get(id)
    if task is None:
        return jsonify(None), 404

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    response = {
        "task": task.to_dict()
    }
    return jsonify(response), 200


@tasks_bp.route("/<id>", methods=["DELETE"])
def delete_one_task(id):
    task = Task.query.get(id)
    if task is None:
        return jsonify(None), 404

    db.session.delete(task)
    db.session.commit()

    response = {
        'details': f'Task {task.id} "{task.title}" successfully deleted'
    }
    return jsonify(response), 200


def slack_chat_post_message(task):
    url = "https://slack.com/api/chat.postMessage"
    auth_token = os.environ.get("AUTHORIZATION_TOKEN")
    auth = f"Bearer {auth_token}"
    channel_id = "task-notifications"
    text = f"Someone just completed the task {task.title}"

    result = requests.post(url, headers=dict(
        authorization=auth), data=dict(channel=channel_id, text=text))


@tasks_bp.route("/<id>/mark_complete", methods=["PATCH"])
def update_task_completed(id):
    task = Task.query.get(id)
    if task is None:
        return jsonify(None), 404

    task.completed_at = date.today()
    db.session.commit()

    response = {
        "task": task.to_dict()
    }
    slack_chat_post_message(task)

    return jsonify(response), 200


@tasks_bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def update_task_not_completed(id):
    task = Task.query.get(id)
    if task is None:
        return jsonify(None), 404

    task.completed_at = None
    db.session.commit()

    response = {
        "task": task.to_dict()
    }
    return jsonify(response), 200


@goals_bp.route("", methods=["GET"])
def read_goals():
    goals = Goal.query.all()
    goals_response = []
    for goal in goals:
        goals_response.append({
            "id": goal.id,
            "title": goal.title
        })

    return jsonify(goals_response), 200


@goals_bp.route("", methods=["POST"])
def add_goal():
    request_body = request.get_json()

    try:
        new_goal = Goal(title=request_body["title"])

        db.session.add(new_goal)
        db.session.commit()

        response = {
            "goal": {
                "id": new_goal.id,
                "title": new_goal.title,
            }
        }
        return jsonify(response), 201

    except KeyError:
        return jsonify({"details": "Invalid data"}), 400


@goals_bp.route("/<id>", methods=["GET"])
def read_one_goal(id):
    goal = Goal.query.get(id)
    if goal is None:
        return jsonify(None), 404

    return {
        "goal": {
            "id": goal.id,
            "title": goal.title
        }
    }


@goals_bp.route("/<id>", methods=["DELETE"])
def delete_one_goal(id):
    goal = Goal.query.get(id)
    if goal is None:
        return jsonify(None), 404

    db.session.delete(goal)
    db.session.commit()

    response = {
        'details': f'Goal {goal.id} "{goal.title}" successfully deleted'
    }
    return jsonify(response), 200


@goals_bp.route("/<id>", methods=["PUT"])
def update_a_goal(id):
    goal = Goal.query.get(id)
    if goal is None:
        return jsonify(None), 404

    request_body = request.get_json()
    goal.title = request_body["title"]

    db.session.commit()

    response = {
        "goal": {
            "id": goal.id,
            "title": goal.title
        }
    }
    return jsonify(response), 200


@goals_bp.route("/<id>/tasks", methods=["POST"])
def link_task_to_goal(id):
    request_body = request.get_json()
    tasks = []

    task_ids = request_body["task_ids"]
    for task_id in task_ids:
        task = Task.query.get(task_id)
        tasks.append(task)

    goal = Goal.query.get(id)
    goal.tasks = tasks

    db.session.commit()

    response = {
        "id": goal.id,
        "task_ids": request_body["task_ids"]
    }

    return jsonify(response)


@goals_bp.route("/<id>/tasks", methods=["GET"])
def read_tasks_from_goal(id):
    goal = Goal.query.get(id)
    if goal is None:
        return jsonify(None), 404

    tasks_response = []
    for task in goal.tasks:
        tasks_response.append(task.to_dict())

    response_body = {
        "id": goal.id,
        "title": goal.title,
        "tasks": tasks_response
    }

    return jsonify(response_body)


# potential refactors:
    # formating of the resopnse {task :  {}} repeated throughout, as well as {details: "fka;df"}


    # LIST COMPREHENSIONS:
    # /goal/id/tasks POST endpoint
