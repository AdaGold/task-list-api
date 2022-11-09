from app import db
from app.models.goal import Goal
from app.models.task import Task
from app.task_routes import validate_id, validate_request_body
from flask import Blueprint, request, make_response, jsonify

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    
    new_goal = validate_request_body(Goal, request_body)

    db.session.add(new_goal)
    db.session.commit()

    return make_response(jsonify({"goal": new_goal.to_dict()}), 201)

@goals_bp.route("", methods=["GET"])
def read_all_goals():
    goals = Goal.query.all()
    goals_response = [goal.to_dict() for goal in goals]

    return jsonify(goals_response)

@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_id(Goal, goal_id)

    return make_response(jsonify({"goal": goal.to_dict()}))

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_id(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    db.session.commit()

    return make_response(jsonify({"goal": goal.to_dict()}))

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_id(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response({"details":f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"})

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_tasks_to_goal(goal_id):
    goal = validate_id(Goal, goal_id)
    request_body = request.get_json()

    task_ids_list = request_body["task_ids"]
    for id in task_ids_list:
        task = validate_id(Task, id)
        task.goal_id = goal_id
    
    db.session.commit()

    return make_response(jsonify({"id": goal.goal_id, "task_ids": task_ids_list}))

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_for_goal(goal_id):
    goal = validate_id(Goal, goal_id)

    tasks_response = [task.to_dict_with_goal() for task in goal.tasks]
            
    return make_response(jsonify({"id": goal.goal_id, "title": goal.title, "tasks": tasks_response}))
