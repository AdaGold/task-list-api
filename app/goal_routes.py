from flask import Blueprint, jsonify, make_response, abort, request, session
from app import db
from app.models.goal import Goal
from app.models.task import Task
from .task_routes import validate_model

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

######## POST GOAL ########################
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

########## GET GOAL ############################
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

######## PUT GOAL ############################
@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    request_body = request.get_json()
    
    goal.title = request_body["title"]
    
    db.session.commit()
    return jsonify({'goal': goal.to_dict()}), 200

######## DELETE GOAL ################################
@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    db.session.delete(goal)
    db.session.commit()
    
    return jsonify({"details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'})

######## POST ONE-TO-MANY TASKS ####################
@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_goal_with_tasks(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    task_ids = request_body["task_ids"]
    
    for task_id in task_ids:
        current_task = validate_model(Task, task_id)
        current_task.goal_id = goal.goal_id
    
    db.session.commit()
    return jsonify({"id": goal.goal_id, "task_ids": task_ids}), 200

####### GET ONE-TO-MANY TASKS ###############################
@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def read_tasks_from_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    return jsonify(goal.to_dict(has_tasks=True)), 200