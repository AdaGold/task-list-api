from flask import Blueprint, jsonify, make_response, abort, request
from app import db
from app.models.goal import Goal
from .routes import validate_model

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal.from_dict(request_body)
    except KeyError:
        return jsonify({'details': 'Invalid data'}), 400

    db.session.add(new_goal)
    db.session.commit()

    return jsonify({'goal': new_goal.to_dict()}), 201

@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return jsonify({'goal': goal.to_dict()}), 200

@goals_bp.route("", methods=["GET"])
def read_all_goals():
    goals = Goal.query.all()

    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())
    return jsonify(goals_response), 200

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    request_body = request.get_json()
    
    goal.title = request_body["title"]
    
    db.session.commit()
    return jsonify({'goal': goal.to_dict()}), 200

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    db.session.delete(goal)
    db.session.commit()
    
    return jsonify({"details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'})
