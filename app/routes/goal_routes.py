from flask import Blueprint, request, abort, make_response
from app.models.goal import Goal
from app.models.task import Task
from app.routes.route_utilities import create_model, validate_model
from app.db import db

bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

@bp.post("")
def create_goal():
    response = create_model(Goal, request.get_json())
    return {"goal": response}, 201


@bp.post("/<goal_id>/tasks")
def create_task_ids_by_goal(goal_id):
    request_body = request.get_json()
    goal = validate_model(Goal, goal_id)

    try:
        task_ids = request_body["task_ids"]
        for task_id in task_ids:
            task = validate_model(Task, task_id)
            goal.tasks.append(task)
        
        db.session.commit()
    
    except KeyError as error:
        response = {"details": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))
        
    return {"id": goal.id, "task_ids": task_ids}
    

@bp.get("")
def get_goals():
    query = db.select(Goal).order_by(Goal.id)
    goals = db.session.scalars(query)

    return [goal.to_dict() for goal in goals]


@bp.get("/<goal_id>")
def get_goal_by_id(goal_id):
    goal = validate_model(Goal, goal_id)
    return {"goal": goal.to_dict()}


@bp.get("/<goal_id>/tasks")
def get_tasks_by_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    goal_dict = goal.to_dict()
    goal_dict["tasks"] = [task.to_dict() for task in goal.tasks]
    
    return goal_dict


@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()
    try:
        goal.title = request_body["title"]
        db.session.commit()

    except KeyError as error:
        response = {"details": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))

    return {"goal": goal.to_dict()}


@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    response = f"Goal {goal_id} \"{goal.title}\" successfully deleted"

    return {"details": response}