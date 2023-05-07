from sqlalchemy import asc, desc
from app import db
from app.models.goal import Goal
from app.models.task import Task
from datetime import datetime
from flask import Blueprint, jsonify, make_response, request, abort

def get_valid_item_by_id(model, id):
    try:
        id = int(id)
    except:
        abort(make_response({'details': "Invalid data"}, 400))

    item = model.query.get(id)
    return item if item else abort(make_response({'message': f"Goal {id} not found"}, 404))


goal_bp = Blueprint("goals", __name__, url_prefix="/goals")


@goal_bp.route("", methods=["POST"])
def create_goal():
    
    # To be able to read the request we need to use the .getj_son() method
    request_body = request.get_json()

    if not "title" in request_body:
        return make_response({"details": "Invalid data"}, 400)

    new_goal = Goal.dict_for_post_method(request_body)
    db.session.add(new_goal)
    db.session.commit()

    return {"goal": new_goal.to_dict()}, 201


@goal_bp.route("", methods=["GET"])
def get_all_goals():

    # get 1 goal by param
    query_request = request.args.get("sort")
    if query_request == "asc":
        goals = Goal.query.order_by(Goal.title.asc())
    elif query_request == "desc":
        goals = Goal.query.order_by(Goal.title.desc())
    # get all Goals
    else:
        goals = Goal.query.all()

    goals_response = []

    for goal in goals:
        goals_response.append(goal.to_dict())
    return jsonify(goals_response), 200

@goal_bp.route("/<goal_id>", methods=["GET"])
def handle_goal(goal_id):
    goal: Goal = get_valid_item_by_id(Goal, goal_id)
    return {"goal": goal.to_dict()}, 200


@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_one_goal(goal_id):

    request_body = request.get_json()
    goal_is_valid: Goal = get_valid_item_by_id(Goal, goal_id)

    goal_is_valid.title = request_body["title"]

    db.session.commit()

    return {"goal": goal_is_valid.to_dict()}, 200


@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_goal(goal_id):
    
    goal_to_delete: Goal = get_valid_item_by_id(Goal, goal_id)

    db.session.delete(goal_to_delete)
    db.session.commit()

    title_goal = goal_to_delete.title

    return {"details": f'Goal {goal_id} "{title_goal}" successfully deleted'}, 200




# ROUTES FOR RELATIONSHIP ONE TO MANY
@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_tasks_to_goal(goal_id):

    request_body = request.get_json()
    goal: Goal = get_valid_item_by_id(Goal, goal_id)
    list_tasks = request_body["task_ids"]

    tasks_list = []

    for task_id in list_tasks:
        task: Task = get_valid_item_by_id(Task, task_id)
        goal.tasks.append(task)
        tasks_list.append(task.task_id)

    db.session.commit()

    return jsonify({"id": goal.goal_id, "task_ids": tasks_list})


# Get tasks for specific goal
@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def handle_tasks_for_specific_goal(goal_id):

    goal: Goal = get_valid_item_by_id(Goal, goal_id)

    return jsonify({
                "id": goal.goal_id,
                "title": goal.title,
                "tasks": goal.tasks_dict()
                }), 200
