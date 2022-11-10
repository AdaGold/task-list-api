from flask import Blueprint, jsonify, request, make_response, abort
from app.models.goal import Goal
from app.routes.task_routes import validate_model_by_id
from app.models.task import Task
from app import db

goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

# POST routes
@goal_bp.route("", methods=["POST"])
def create_one_goal():
    request_body = request.get_json()

    try:
        new_goal = Goal.from_dict(request_body)
    except KeyError:
        return abort(make_response(jsonify({"details": "Invalid data"}), 400))

    db.session.add(new_goal)
    db.session.commit()

    return jsonify({"goal": new_goal.to_dict()}), 201


@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_task_ids_to_goal(goal_id):
    goal_to_update = validate_model_by_id(Goal, goal_id)
    response_body = request.get_json()

    task_list = []

    for task_id in response_body["task_ids"]:
        validated_task = validate_model_by_id(Task, task_id)
        task_list.append(validated_task.task_id)
        validated_task.goal = goal_to_update
        db.session.commit()

    return jsonify({
        "id": goal_to_update.goal_id, 
        "task_ids":response_body["task_ids"]
        }), 200


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


@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_for_goal(goal_id):
    goal = validate_model_by_id(Goal, goal_id)
    tasks = goal.get_tasks_list()

    return jsonify(goal.to_dict_with_goal_id()), 200


# PUT route
@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_one_goal(goal_id):
    update_goal = validate_model_by_id(Goal, goal_id)
    request_body = request.get_json()

    try:
        update_goal.title = request_body["title"]
    except KeyError:
        return abort(make_response(jsonify({"message":"KeyError: Missing data needed"}),400))

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