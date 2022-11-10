from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, make_response, request, abort
from datetime import date
import requests, os
from .routes_helper import validate_model


goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def create_goal():

    request_body = request.get_json()
    
    if "title" not in request_body:
            abort(make_response({"details": "Invalid data" }, 400))

    new_goal = Goal(
        title=request_body["title"],
        )

    db.session.add(new_goal)
    db.session.commit()
    
    return ({"goal": new_goal.to_dict()}, 201)

@goals_bp.route("", methods=["GET"])
def get_all_goals():  

    goals = Goal.query.all()

    goals_response = [goal.to_dict() for goal in goals]

    return jsonify(goals_response)

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return {"goal": goal.to_dict()}

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    db.session.delete(goal)
    db.session.commit()

    return ({
    "details": f'Goal {goal_id} "{goal.title}" successfully deleted'
    }, 200)

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    goal.title = request_body["title"]
    
    db.session.commit()

    return {"goal": goal.to_dict()}

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def merge_task_with_goal(goal_id):

    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    task_id_list = request_body['task_ids']

    for task_id in task_id_list:
        task = validate_model(Task, task_id)
        task.goal_id = goal_id

    db.session.commit()
    
    return {
        "id": goal.goal_id,
        "task_ids": task_id_list
    }

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_for_goal(goal_id):
    
    tasks = Task.query.all()
    goal = validate_model(Goal, goal_id)

    tasks_response = [{"id": task.task_id, "goal_id": goal.goal_id, "title": task.title, "description": task.description, "is_complete": False} for task in tasks]

    return {
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": tasks_response
    }
