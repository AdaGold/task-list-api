from flask import Blueprint, request, abort, make_response,Response
from ..db import db
from ..models.goal import Goal
from ..models.task import Task
from .route_utilities import validate_model,create_model,get_models_with_filters

bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@bp.post("")
def create_goal():
    request_body = request.get_json()
  
    return create_model(Goal,request_body)

@bp.get("")
def get_all_goals():
   filters = request.args.to_dict()
   return get_models_with_filters(Goal,filters)

@bp.get("/<id>")
def get_one_goal(id):
    goal = validate_model(Goal, id)
    return goal.to_dict()

@bp.put("/<id>")
def update_goal(id):
    goal = validate_model(Goal, id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()
    return goal.to_dict()

@bp.delete("/<id>")
def delete_goal(id):
    goal = validate_model(Goal, id)

    db.session.delete(goal)
    db.session.commit()
    
    return Response(status=204, mimetype="application/json")

#nested
@bp.post("/<goal_id>/tasks")
def add_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    task_ids = request_body.get("task_ids", [])
    
    for task in goal.tasks:
        task.goal_id = None

    for task_id in task_ids:
        task = validate_model(Task, task_id)
        task.goal_id = goal.id

    db.session.commit()

    return {
        "id": goal.id,
        "task_ids": task_ids
    }, 200
       
@bp.get("/<goal_id>/tasks")
def get_tasks_for_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    tasks_response = [task.to_dict() for task in goal.tasks]

    response_body = {
        "id": goal.id,
        "title": goal.title,
        "tasks": tasks_response
    }
    
    return response_body,200

    
    
