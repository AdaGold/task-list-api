from flask import Blueprint, request, make_response, jsonify, abort
from app import db
from app.models.goal import Goal
from app.models.task import Task

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        return {"details": "Invalid data"}, 400

    new_goal = Goal(
        title=request_body["title"]
    )

    db.session.add(new_goal)
    db.session.commit()

    # return {"goal": {
    #     "id": new_goal.goal_id,
    #     "title": new_goal.title
    # }}, 201

    return jsonify({"goal": new_goal.to_dict()}), 201


def validated_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except ValueError:
        rsp = {"msg": f"Invalid id: {goal_id}"}
        abort(make_response(jsonify(rsp), 400))

    goal = Goal.query.get(goal_id)

    if goal is None:
        rsp = {"msg":f"Goal {goal_id} not found"}
        abort(make_response(jsonify(rsp), 404))

    return goal

def validated_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        rsp = {"msg": f"Invalid id: {task_id}"}
        abort(make_response(jsonify(rsp), 400))

    task = Task.query.get(task_id)

    if task is None:
        rsp = {"message":f"Task {task_id} not found"}
        abort(make_response(jsonify(rsp), 404))

    return task

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    chosen_goal = validated_goal(goal_id)

    return jsonify(
        {"goal": {
        "id": chosen_goal.goal_id,
        "title": chosen_goal.title,}}), 200

@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()

    goals_response = []
    for goal in goals:
        goals_response.append({
            "id": goal.goal_id,
            "title": goal.title,
        })

    return jsonify(goals_response)

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    # goal = Goal.query.get(goal_id)
    goal = validated_goal(goal_id)
    request_body = request.get_json()
    goal.title = request_body["title"]

    db.session.commit()

    return {"goal": {
        "id": goal.goal_id,
        "title": goal.title,
    }}, 200

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_goal(goal_id):
    
    goal = validated_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return jsonify({"details": f'Goal "{goal.title}" successfully deleted'}), 200


@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def goal_to_task(goal_id):
    goal = validated_goal(goal_id)
    request_body = request.get_json()

    for task_id in request_body["task_ids"]:
        task = validated_task(task_id)
    
        goal.tasks.append(task)

    # db.session.add(task)
    db.session.commit()

    return {
        "id": goal.goal_id,
        "task_ids": request_body["task_ids"]
    }, 200

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_goal_task(goal_id):
    goal = validated_goal(goal_id)
    result = {
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": []
    }

    for task in goal.tasks:
        result["tasks"].append(task.to_dict())

    return result, 200







