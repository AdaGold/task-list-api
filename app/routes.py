from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, request, jsonify
from datetime import datetime
import os
import requests
from functools import wraps

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


def validate_task(f):
    @wraps(f)
    def decorated_function(*args, id, **kwargs):
        task = Task.query.get(id)
        if not task:
            return jsonify(None), 404
        return f(*args, task, **kwargs)
    return decorated_function

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title)
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
    response_body = [task.to_dict() for task in tasks]
    return jsonify(response_body), 200

@tasks_bp.route("", methods=["POST"])
def create_new_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
        return {"details": "Invalid data"}, 400

    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    response_body={
        "task": new_task.to_dict()
    }

    return jsonify(response_body), 201

@tasks_bp.route("/<id>", methods=["GET"])
@validate_task
def get_one_task(task):
    return {
        "task": task.to_dict()
    }

@tasks_bp.route("/<id>", methods=["PUT"])
@validate_task
def edit_one_task(task):
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body.get("completed_at")

    db.session.commit()

    return {
        "task": task.to_dict()
    }

@tasks_bp.route("/<id>", methods=["DELETE"])
@validate_task
def delete_one_task(task):
    db.session.delete(task)
    db.session.commit()

    return {
        "details": f"Task {task.id} \"{task.title}\" successfully deleted"
    }


@tasks_bp.route("/<id>/<status>", methods=["PATCH"])
@validate_task
def change_one_task_status(task, status):

    if status == "mark_complete":
        task.completed_at = datetime.now()

        data = {
            "token": os.environ.get("SLACK_BOT_TOKEN"),
            "channel": "task-notifications",
            "text": f"Someone just complete the task {task.title}"
        }
        requests.post("https://slack.com/api/chat.postMessage", data=data)

    elif status == "mark_incomplete":
        task.completed_at = None

    else:
        return jsonify(None), 404

    db.session.commit()

    return {
        "task": task.to_dict()
    }


@goals_bp.route("", methods=["GET", "POST"])
def goals():
    if request.method == "GET":
        goals = Goal.query.all()
        response_body = [goal.to_dict() for goal in goals]
        return jsonify(response_body), 200

    elif request.method == "POST":
        request_body = request.get_json()

        if "title" not in request_body:
            return jsonify({"details": "Invalid data"}), 400

        new_goal = Goal.from_dict(request_body)

        db.session.add(new_goal)
        db.session.commit()

        response_body = {
            "goal": new_goal.to_dict()
        }

        return jsonify(response_body), 201

@goals_bp.route("/<id>", methods=["GET", "PUT", "DELETE"])
def goal_id(id):
    goal = Goal.query.get(id)

    if not goal:
        return jsonify(None), 404

    if request.method == "GET":
        response_body = {
            "goal": goal.to_dict()
        }
        return jsonify(response_body), 200

    elif request.method == "PUT":
        request_body = request.get_json()
        goal.title = request_body["title"]

        db.session.commit()

        response_body = {
            "goal": goal.to_dict()
        }

        return jsonify(response_body), 200

    elif request.method == "DELETE":
        db.session.delete(goal)
        db.session.commit()

        response_body = {
            "details": f"Goal {id} \"{goal.title}\" successfully deleted"
        }

        return jsonify(response_body), 200

@goals_bp.route("/<id>/tasks", methods=["GET", "POST"])
def goal_id_tasks(id):
    goal = Goal.query.get(id)

    if not goal:
        return jsonify(None), 404

    if request.method == "GET":
        # tasks = []
        # for task in goal.tasks:
        #     task_dict = task.to_dict()
        #     task_dict.update({"goal_id": goal.id})
        #     tasks.append(task_dict)

        # goal_dict = goal.to_dict()
        # goal_dict.update({"tasks": tasks})

        # return goal_dict, 200

        return goal.to_dict(tasks=True), 200

    elif request.method == "POST":
        try:
            task_ids = request.get_json()["task_ids"]
        except KeyError:
            return jsonify("test"), 400

        for task_id in task_ids:
            task = Task.query.get(task_id)
            task.goal = goal

        db.session.commit()

        response_body = {
            "id": goal.id,
            "task_ids": task_ids
        }

        return jsonify(response_body), 200
