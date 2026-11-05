from flask import Blueprint, request, Response
from app.models.goal import Goal
from app.models.task import Task
from app.db import db
from .routes_yay import validate_model, create_model

goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

@goal_bp.post("")
def create_goal():
    request_body = request.get_json()
    return create_model(Goal, request_body)

@goal_bp.get("")
def get_all_goals():
    query = db.select(Goal).order_by(Goal.id)
    goals = db.session.scalars(query)

    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())
    return goals_response

@goal_bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return goal.to_dict()

@goal_bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@goal_bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@goal_bp.post("/<goal_id>/tasks")
def post_task_ids_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    tasks = []
    for task_id in request_body["task_ids"]:
        task = validate_model(Task, task_id)
        tasks.append(task)

    goal.tasks = tasks
    db.session.commit()

    return {"id": goal.id, "task_ids": request_body["task_ids"]}

@goal_bp.get("/<goal_id>/tasks")
def get_tasks_for_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    tasks_response = []
    for task in goal.tasks:
        tasks_response.append(task.to_dict())

    response = goal.to_dict()
    response["tasks"] = tasks_response
    return response