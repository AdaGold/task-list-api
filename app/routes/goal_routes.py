from flask import Blueprint, request, abort, make_response, Response
from .route_utilities import validate_model
from app.models.goal import Goal
from app.models.task import Task
from ..db import db


bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@bp.get("")
def get_all_goals():
    query = db.select(Goal)
    goals = db.session.scalars(query)
    goals_response = [goal.to_dict() for goal in goals]
    return goals_response


@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return {"goal": goal.to_dict()}


@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    goal.title = request_body["title"]

    db.session.add(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.post("")
def create_goal():
    request_body = request.get_json()

    try:
        new_goal = Goal.from_dict(request_body)

    except KeyError as error:
        response = {"details": f"Invalid data"}
        abort(make_response(response, 400))

    db.session.add(new_goal)
    db.session.commit()

    return {"goal": new_goal.to_dict()}, 201


@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.get("/<goal_id>/tasks")
def get_tasks_from_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    tasks = [task.to_dict() for task in goal.tasks]
    
    response = goal.to_dict()
    response["tasks"] = tasks
    return response


@bp.post("/<goal_id>/tasks")
def add_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    task_ids = request_body["task_ids"]

    tasks = [validate_model(Task, task_id) for task_id in task_ids]
    goal.tasks = tasks

    db.session.commit()

    response = {
        "id": goal.id,
        "task_ids": [task.id for task in goal.tasks],
    }
    return response