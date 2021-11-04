from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, request, jsonify
from functools import wraps


goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


def validate_goal(f):
    @wraps(f)
    def decorated_function(id):
        goal = Goal.query.get(id)
        if not goal:
            return jsonify(None), 404
        return f(goal)
    return decorated_function


@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()
    response_body = [goal.to_dict() for goal in goals]
    return jsonify(response_body)


@goals_bp.route("", methods=["POST"])
def create_new_goal():
    request_body = request.get_json()

    if not request_body.get("title") or len(request_body) != 1:
        return details(invalid_msg()), 400

    new_goal = Goal.from_dict(request_body)
    db.session.add(new_goal)
    db.session.commit()
    return response(new_goal), 201


@goals_bp.route("/<id>", methods=["GET"])
@validate_goal
def get_one_goal(goal):
    return response(goal)


@goals_bp.route("/<id>", methods=["PUT"])
@validate_goal
def edit_one_goal(goal):
    request_body = request.get_json()

    if not request_body.get("title"):
        return details(invalid_msg()), 400

    goal.title = request_body["title"]
    db.session.commit()
    return response(goal)


@goals_bp.route("/<id>", methods=["DELETE"])
@validate_goal
def delete_one_goal(goal):
    db.session.delete(goal)
    db.session.commit()
    return details(delete_msg(goal))


@goals_bp.route("/<id>/tasks", methods=["GET"])
@validate_goal
def get_tasks_for_one_goal(goal):
    return goal.to_dict(tasks=True), 200


@goals_bp.route("/<id>/tasks", methods=["POST"])
@validate_goal
def add_tasks_to_one_goal(goal):
    try:
        task_ids = request.get_json()["task_ids"]
    except KeyError:
        return details(invalid_msg()), 400

    valid_task_ids = []
    for task_id in task_ids:
        task = Task.query.get(task_id)
        if task:
            task.goal = goal
            valid_task_ids.append(task_id)

    db.session.commit()
    return {
        "id": goal.id,
        "task_ids": valid_task_ids
    }


def response(goal):
    return {"goal": goal.to_dict()}


def details(msg):
    return {"details": msg}


def delete_msg(goal):
    return f'Goal {goal.id} "{goal.title}" successfully deleted'


def invalid_msg():
    return "Invalid data"
