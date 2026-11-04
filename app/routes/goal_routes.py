from flask import Blueprint, abort, make_response, request, Response
from app.models.goal import Goal
from app.models.task import Task
from app.db import db
from .task_routes import validate_task

goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

@goal_bp.post("")
def create_goal():
    request_body = request.get_json()

    try:
        new_goal = Goal.from_dict(request_body)
    except KeyError:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))

    db.session.add(new_goal)
    db.session.commit()

    return new_goal.to_dict(), 201

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
    goal = validate_goal(goal_id)
    return goal.to_dict()

@goal_bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@goal_bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_goal(goal_id)
    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@goal_bp.post("/<goal_id>/tasks")
def post_task_ids_to_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()

    tasks = []
    for task_id in request_body["task_ids"]:
        task = validate_task(task_id)
        tasks.append(task)

    goal.tasks = tasks
    db.session.commit()

    return {"id": goal.id, "task_ids": request_body["task_ids"]}

@goal_bp.get("/<goal_id>/tasks")
def get_tasks_for_goal(goal_id):
    goal = validate_goal(goal_id)

    tasks_response = []
    for task in goal.tasks:
        tasks_response.append(task.to_dict())

    response = goal.to_dict()
    response["tasks"] = tasks_response
    return response

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        response = {"message": f"goal {goal_id} invalid"}
        abort(make_response(response, 400))

    query = db.select(Goal).where(Goal.id == goal_id)
    goal = db.session.scalar(query)

    if not goal:
        response = {"message": f"goal {goal_id} not found"}
        abort(make_response(response, 404))

    return goal