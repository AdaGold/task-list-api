from app import db
from app.models.goal import Goal
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

# CREATE
@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    created_goal = {"goal": new_goal.to_dict()}
    return make_response(created_goal, 201)

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