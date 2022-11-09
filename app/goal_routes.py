from flask import Blueprint, jsonify, request, abort, make_response
from app.models.goal import Goal
from app.routes import validate_model_by_id
from app import db
from datetime import datetime
import requests, os
from dotenv import load_dotenv

goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

# GET routes
@goal_bp.route("", methods=["GET"])
def get_all_goals():

    goals = Goal.query.all()
    
    goals_response = [goal.to_dict() for goal in goals]

    return jsonify(goals_response), 200


# @goal_bp.route("/<goal_id>", methods=["GET"])
# def get_one_goal(goal_id):
#     goal = validate_model_by_id(Goal, goal_id)

# Don't forget to register blueprints