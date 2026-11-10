from flask import Blueprint, request, jsonify
from ..db import db
from ..models.goal import Goal
from ..models.task import Task
from .route_utilities import JSONBadRequest, validate_model, create_model


goals_bp = Blueprint("goals", __name__)


@goals_bp.route("/goals", methods=["POST"])
def create_goal():
    request_body = request.get_json(silent=True)

    return create_model(Goal, request_body)


@goals_bp.route("/goals", methods=["GET"])
def get_goals():
    goals = db.session.execute(db.select(Goal)).scalars().all()

    goals_list = []

    for goal in goals:
        goals_list.append(goal.to_dict())

    return jsonify(goals_list), 200


@goals_bp.route("/goals/<int:goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return jsonify(goal.to_dict()), 200


@goals_bp.route("/goals/<int:goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json(silent=True)

    if not isinstance(request_body, dict) or not request_body.get("title"):
        raise JSONBadRequest(description="Invalid data") 

    goal.title = request_body["title"]
    db.session.commit()

    return "", 204, {"Content-Type": "application/json"}


@goals_bp.route("/goals/<int:goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return "", 204, {"Content-Type": "application/json"}


@goals_bp.route("/goals/<int:goal_id>/tasks", methods=["POST"])
def add_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json(silent=True)

    if not isinstance(request_body, dict):
        return jsonify({"details": "Invalid data"}), 400

    task_ids = request_body.get("task_ids")

    if not isinstance(task_ids, list):
        return jsonify({"details": "Invalid data"}), 400

    tasks = []

    for task_id in task_ids:
        if type(task_id) is not int:
            return jsonify({"details": "Invalid task ID"}), 400

        task = db.session.get(Task, task_id)

        if task is None:
            return jsonify({"details": "Task not found"}), 404

        tasks.append(task)

    goal.tasks = tasks
    db.session.commit()

    return jsonify({
        "id": goal.id,
        "task_ids": task_ids
    }), 200


@goals_bp.route("/goals/<int:goal_id>/tasks", methods=["GET"])
def get_tasks_for_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    tasks_list = []

    for task in goal.tasks:
        tasks_list.append(task.to_dict(include_goal=True))

    return jsonify({
        "id": goal.id,
        "title": goal.title,
        "tasks": tasks_list
    }), 200