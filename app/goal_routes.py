from flask import Blueprint, jsonify, request, abort, make_response
from app.models.goal import Goal
from app.routes import validate_model_by_id
from app import db
from datetime import datetime
import requests, os
from dotenv import load_dotenv

goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

# POST route
@goal_bp.route("", methods=["POST"])
def create_one_goal():
    request_body = request.get_json()

    try:
        new_goal = Goal.from_dict(request_body)
    except KeyError:
        return jsonify({"details": "Invalid data"}), 400

    db.session.add(new_goal)
    db.session.commit()

    return jsonify({"goal": new_goal.to_dict()}), 201

# GET routes
@goal_bp.route("", methods=["GET"])
def get_all_goals():

    goals = Goal.query.all()
    
    goals_response = [goal.to_dict() for goal in goals]

    return jsonify(goals_response), 200


@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_model_by_id(Goal, goal_id)

    return jsonify({"goal": goal.to_dict()}), 200


# PUT route
@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_one_goal(goal_id):
    update_goal = validate_model_by_id(Goal, goal_id)
    request_body = request.get_json()

    update_goal.title = request_body["title"]

    db.session.commit()

    return jsonify({"goal": update_goal.to_dict()}), 200


# DELETE route
@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model_by_id(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response(jsonify({
        "details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'
    }))