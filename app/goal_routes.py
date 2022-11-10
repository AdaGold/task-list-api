from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task
from app.models.goal import Goal
from app.routes import validate_model


goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def create_goal_():
    request_body = request.get_json()

    if not "title" in request_body:
        return {"details" : "Invalid data"}, 400

    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()
    return {"goal": new_goal.to_dict()}, 201


@goals_bp.route("", methods=["GET"])
def get_goals():
    goals = Goal.query.all()
    goal_response = [goal.to_dict() for goal in goals]

    return jsonify(goal_response)


@goals_bp.route("/<id>", methods=["GET"])
def get_one_goal(id):
    goal = validate_model(Goal, id)
    return {"goal": goal.to_dict()}, 200


@goals_bp.route("/<id>", methods=["PUT"])
def update_goal(id):
    goal = validate_model(Goal, id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return {"goal": goal.to_dict()}, 200

@goals_bp.route("/<id>", methods=["DELETE"])
def delete_goal(id):
    goal = validate_model(Goal, id)

    db.session.delete(goal)
    db.session.commit()

    return {"details": f'Goal {goal.id} "{goal.title}" successfully deleted'}


@goals_bp.route("/<id>/tasks", methods=["POST"])
def post_task_ids_to_goal(id):
    goal = validate_model(Goal, id)
    request_body = request.get_json()
    
    for task_id in request_body["task_ids"]:
        task = validate_model(Task, task_id)
        goal.tasks.append(task)
    
    db.session.commit()

    return {"id": goal.id, "task_ids": request_body["task_ids"]}, 200


@goals_bp.route("/<id>/tasks", methods=["GET"])
def get_tasks_for_specific_goal(id):
    goal = validate_model(Goal, id)

    tasks_response = [task.to_dict() for task in goal.tasks]
    
    # for task in goal.tasks:
    #     tasks_response.append(task.to_dict())
    return {"id": goal.id, "title": goal.title,  "tasks": tasks_response}, 200

