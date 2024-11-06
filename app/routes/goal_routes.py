from flask import Blueprint, request, abort, make_response
from app.models.goal import Goal
from app.routes.route_utilities import create_model, validate_model
from app.db import db

bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

@bp.post("")
def create_goal():
    response = create_model(Goal, request.get_json())
    return {"goal": response}, 201


@bp.get("")
def get_all_goals():
    query = db.select(Goal).order_by(Goal.id)
    goals = db.session.scalars(query)

    return [goal.to_dict() for goal in goals]


@bp.get("/<goal_id>")
def get_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return {"goal": goal.to_dict()}


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

    response = f"Goal {goal_id} {goal.title} successfully deleted"

    return {"details": response}