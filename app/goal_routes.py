from app import db
from app.models.goal import Goal
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request

goal_bp = Blueprint("goals", __name__, url_prefix="/goals")


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except: 
        abort(make_response({"details":"Invalid data"}, 400))

    model = cls.query.get(model_id)
    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model 

@goal_bp.route("", methods=["POST"])
def create_goal():
    try:
        request_body = request.get_json()
        new_goal = Goal.from_dict(request_body)
    except:
        abort(make_response({"details":"Invalid data"}, 400))

    db.session.add(new_goal)
    db.session.commit()

    return make_response(jsonify({
            "goal": Goal.to_dict(new_goal)})), 201

@goal_bp.route("", methods=["GET"])
def read_all_goals():
    goals_query = Goal.query
    goals = goals_query.all()
    goals_response = [goal.to_dict() for goal in goals]
    
    return jsonify(goals_response), 200

@goal_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    result_goal = validate_model(Goal, goal_id)
    return jsonify({
            "goal": result_goal.to_dict()}), 200

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return make_response(jsonify({
            "goal": goal.to_dict()})), 200

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response(jsonify({
    "details": f"Goal {goal_id} \"{goal.title}\" successfully deleted"
}))

@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_task(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    
    task_ids= []
    for task in request_body["task_ids"]:
        new_task = validate_model(Task, task)
        task_ids.append(task)

        new_task.goal = goal

    db.session.add(new_task)
    db.session.commit()

    return make_response({
        "id": int(goal_id),
        "task_ids": request_body["task_ids"]
    }), 200




@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def read_tasks(goal_id):
    goal = validate_model(Goal, goal_id)

    task_response = []

    for task in goal.tasks:
        task_response.append(task.task_dict())
    
    return {
        "id": int(goal_id),
        "title": goal.title,
        "tasks": task_response
    }