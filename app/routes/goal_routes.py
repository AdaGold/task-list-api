
from flask import Blueprint, request, abort, make_response, Response
from ..db import db
from ..models.goal import Goal
from ..models.task import Task
from .route_utilities import validate_model, create_model


bp = Blueprint("goals", __name__)


@bp.post("/goals")
def create_goal():
    request_body = request.get_json()

    return create_model(Goal, request_body)


@bp.get("/goals")
def get_goals():
    goals = db.session.execute(db.select(Goal)).scalars()

    goals_list = []

    for goal in goals:
        goals_list.append(goal.to_dict())

    return goals_list, 200


@bp.get("/goals/<int:goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return goal.to_dict(), 200


@bp.put("/goals/<int:goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    if not isinstance(request_body, dict) or not request_body.get("title"):
        abort(make_response(
            {"details": "Invalid data"}, 400
        ))

    goal.title = request_body["title"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.delete("/goals/<int:goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.post("/goals/<int:goal_id>/tasks")
def add_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    if not isinstance(request_body, dict):
        abort(make_response(
            {"details": "Invalid data"}, 400
        ))

    task_ids = request_body.get("task_ids")

    if not isinstance(task_ids, list):
        abort(make_response(
            {"details": "Invalid data"}, 400
        ))

    tasks = []

    for task_id in task_ids:
        if type(task_id) is not int:
            abort(make_response(
                {"details": "Invalid task ID"}, 400
            ))

        task = validate_model(Task, task_id)
        tasks.append(task)

    goal.tasks = tasks
    db.session.commit()

    return {
        "id": goal.id,
        "task_ids": task_ids
    }, 200


@bp.get("/goals/<int:goal_id>/tasks")
def get_tasks_for_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    tasks_list = []

    for task in goal.tasks:
        tasks_list.append(task.to_dict(include_goal=True))

    return {
        "id": goal.id,
        "title": goal.title,
        "tasks": tasks_list
    }, 200
