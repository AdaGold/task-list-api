from app import db
from app.models.goal import Goal
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort

goals_bp = Blueprint("goal", __name__, url_prefix="/goals")

# HELPER FUNCTIONS
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} is not a valid id"}, 400))

    model = cls.query.get(model_id)
    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404))
    
    return model

def validate_request(request_body):
    try:
        request_body["title"]
    except:
        abort(make_response({"details": "Invalid data"}, 400))

# CREATE
@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    validate_request(request_body)
    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    created_goal = {"goal": new_goal.to_dict()}
    return make_response(created_goal, 201)

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_tasks_to_goal(goal_id):
    request_body = request.get_json()
    task_ids = request_body["task_ids"]
    goal = validate_model(Goal, goal_id)

    for task_id in task_ids:
        new_task = validate_model(Task, task_id)
        goal.tasks.append(new_task)
    db.session.add(goal)    
    db.session.commit()

    return make_response({"id": goal.goal_id, "task_ids": task_ids}, 200)

# READ
@goals_bp.route("", methods=["GET"])
def handle_goals():
    goals = Goal.query.all()
    response_body = [goal.to_dict() for goal in goals]

    return jsonify(response_body), 200

@goals_bp.route("/<goal_id>", methods=["GET"])
def handle_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    response_body = {"goal": goal.to_dict()}

    return jsonify(response_body), 200

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_for_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    task_response = [task.to_dict() for task in goal.tasks]
    
    response_body = {
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": task_response
    }

    return jsonify(response_body), 200

# UPDATE
@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    response_body = {"goal": validate_model(Goal, goal_id).to_dict()}

    return make_response(jsonify(response_body)), 200

# DELETE
@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    response_body = f"Goal {goal_id} \"{goal.title}\" successfully deleted"

    db.session.delete(goal)
    db.session.commit()
    
    return make_response({"details": response_body}, 200)