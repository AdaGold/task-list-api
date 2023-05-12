from app.task_routes import validate_model
from os import abort
from app import db
from app.models.goal import Goal
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
from datetime import datetime
import requests
import os
from dotenv import load_dotenv
load_dotenv()

# Instantiate Blueprint instances here
goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")


# *************************************************************************
# ********************************* GOALS *********************************
# *************************************************************************

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    if not "title" in request_body:
        abort(make_response({"details": "Invalid data"}, 400))

    new_goal = Goal(title=request_body["title"])

    db.session.add(new_goal)
    db.session.commit()

    # return make_response(jsonify(f"Task {new_task.title} successfully created"), 201)
    return make_response(jsonify({
        "goal": {
            "id": new_goal.goal_id,
            "title": new_goal.title

        }
    }), 201)


@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()

    goal_response = []
    for goal in goals:
        goal_response.append(
            {
                "id": goal.goal_id,
                "title": goal.title,

            }
        )
    return jsonify(goal_response)


@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return make_response(jsonify({
        "goal": {
            "id": goal.goal_id,
            "title": goal.title,
        }
    }), 200)


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return make_response(jsonify({
        "goal": {
            "id": goal.goal_id,
            "title": goal.title,
        }
    }), 200)


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response(
        {"details": f"Goal {goal_id} \"{goal.title}\" successfully deleted"}, 200)
