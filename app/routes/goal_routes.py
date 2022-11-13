from app import db
from app.models.goal import Goal
from flask import Blueprint, request, jsonify, make_response
from app.routes.task_routes import validate_id

goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

# ================================
# Create one goal 
# ================================

@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    try:
        new_goal = Goal.create(request_body)
    except KeyError:
        return make_response({"details": "Invalid data"}, 400)

    db.session.add(new_goal)
    db.session.commit()

    return jsonify({"goal": new_goal.to_json()}), 201

# ==================================
# Get all goals  
# ==================================

@goal_bp.route("", methods=["GET"])
def get_all_goals():
        all_goals = Goal.query.all()
        results_list = []
        for goal in all_goals:
            results_list.append(goal.to_json())
        return jsonify(results_list), 200

# ==================================
# Get one goal by id number
# ==================================
@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    return jsonify({"goal": validate_id(Goal, goal_id).to_json()}), 200

# ==================================
# Update one goal 
# ==================================
@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_one_goal(goal_id):
    request_body = request.get_json()
    goal = validate_id(Goal, goal_id)
    goal.update(request_body)
    db.session.commit()
    return jsonify({"goal": goal.to_json()}), 200

# ==================================
# Delete one goal by id
# ==================================
@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_goal(goal_id):
    goal = validate_id(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response({"details":f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}, 200)
