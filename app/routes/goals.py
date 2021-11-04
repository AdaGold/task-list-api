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
    return jsonify(response_body), 200

@goals_bp.route("", methods=["POST"])
def create_new_goal():
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

@goals_bp.route("/<id>", methods=["GET"])
@validate_goal
def get_one_goal(goal):
    return {
        "goal": goal.to_dict()
    }

@goals_bp.route("/<id>", methods=["PUT"])
@validate_goal
def edit_one_goal(goal):
    request_body = request.get_json()
    goal.title = request_body["title"]

    db.session.commit()

    return {
        "goal": goal.to_dict()
    }

@goals_bp.route("/<id>", methods=["DELETE"])
@validate_goal
def delete_one_goal(goal):
    db.session.delete(goal)
    db.session.commit()

    return {
        "details": f"Goal {goal.id} \"{goal.title}\" successfully deleted"
    }

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
        return jsonify("test"), 400

    for task_id in task_ids:
        task = Task.query.get(task_id)
        task.goal = goal

    db.session.commit()

    return {
        "id": goal.id,
        "task_ids": task_ids
    }

