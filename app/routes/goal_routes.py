from app import db
from app.models.goal import Goal
from app.models.task import Task
from app.routes.task_routes import get_task_record_by_id
from flask import Blueprint, jsonify, abort, make_response, request
from .routes_helper import error_message
from datetime import datetime
import requests

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

def get_goal_record_by_id(id):
    try:
        id = int(id)
    except:
        abort(make_response({"message":f"goal {id} invalid"}, 400))
    
    goal = Goal.query.get(id)

    if not goal:
        abort(make_response({"message":f"goal {id} not found"}, 404))

    return goal

def make_goal_safely(data_dict):
    try:
        return Goal.from_dict(data_dict)
    except KeyError as err:
        error_message("Invalid data", 400)

# def marked_complete_bot_message(title):
#     path = "https://slack.com/api/chat.postMessage"

#     query_params = {
#         "channel": "goal-list",
#         "text":f"Someone just completed the goal {title}"
#     }

#     call_headers = {"Authorization": "Bearer xoxb-3517483621795-3514864472709-eftmGUbZpBrItU54XIpAnwQo" }

#     api_call_response = requests.post(path, params=query_params, headers=call_headers)

#     return api_call_response

@goals_bp.route("", methods=["GET"])
def read_all_goals():
    sort_param = request.args.get("sort")

    goals = Goal.query.all()

    if sort_param:
        if sort_param:
            titles = []
            for goal in goals:
                titles.append(goal.title)
            if sort_param == "desc":
                sorted_titles = sorted(titles, reverse=True)
            elif sort_param == "asc":
                sorted_titles = sorted(titles)
            sorted_goals = []
            for title in sorted_titles:
                for goal in goals:
                    if goal.title == title:
                        sorted_goals.append(goal)
            goals = sorted_goals
        # elif sort_param == "desc":

    goals_response = []
    for goal in goals:
        goals_response.append(
            {
                "id": goal.id,
                "title": goal.title
            }
        )
    return jsonify(goals_response), 200



@goals_bp.route("/<id>", methods=["GET"])
def read_goal_by_id(id):
    goal = get_goal_record_by_id(id)
    return jsonify({"goal":{
        "id": goal.id,
        "title": goal.title
    }}), 200

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    
    new_goal = make_goal_safely(request_body)

    db.session.add(new_goal)
    db.session.commit()

    response = {"goal":{
        "id":new_goal.id,
        "title":new_goal.title
    }}

    return make_response(jsonify(response), 201)

@goals_bp.route("/<id>", methods=["PUT"])
def replace_goal_by_id(id):
    goal = get_goal_record_by_id(id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    response = {"goal":{
        "id":goal.id,
        "title":goal.title
    }}

    return make_response(jsonify(response), 200)


# @goals_bp.route("/<id>/mark_complete", methods = ["PATCH"])
# def mark_goal_complete_by_id(id):
#     goal = get_goal_record_by_id(id)
#     # goal.is_complete = True
#     # goal.completed_at = datetime.now()

#     db.session.commit()

#     response = {"goal":{
#         "id":goal.id,
#         "title":goal.title
#     }}

#     marked_complete_bot_message(goal.title)
#     #Send bot message
    

#     return make_response(jsonify(response), 200)

# @goals_bp.route("/<id>/mark_incomplete", methods = ["PATCH"])
# def mark_goal_incomplete_by_id(id):
#     goal = get_goal_record_by_id(id)
#     # goal.is_complete = False
#     # goal.completed_at = None

#     db.session.commit()

#     response = {"goal":{
#         "id":goal.id,
#         "title":goal.title
#     }}

#     return make_response(jsonify(response), 200)

@goals_bp.route("/<id>", methods=["DELETE"])
def delete_goal(id):
    goal = get_goal_record_by_id(id)

    db.session.delete(goal)
    db.session.commit()

    return make_response(jsonify({"details":f'Goal {goal.id} "{goal.title}" successfully deleted'}))

@goals_bp.route("/<id>/tasks/create", methods = ["POST"])
def create_task_with_goal(id):
    goal = get_goal_record_by_id(id)
    
    request_body = request.get_json()
    new_task = Task.from_dict(request_body)
    new_task.goal_id = goal.id
    new_task.goal = goal.title

    db.session.add(new_task)
    db.session.commit()

    return jsonify(new_task.to_dict()), 201

@goals_bp.route("/<id>/tasks", methods = ["POST"])
def associate_tasks_with_goal(id):
    goal = get_goal_record_by_id(id)
    
    request_body_ids_list = request.get_json()

    for task_id in request_body_ids_list["task_ids"]:
        task = get_task_record_by_id(task_id) 
        task.goal_id = goal.id

    db.session.commit()

    return jsonify({"id":goal.id, "task_ids": request_body_ids_list["task_ids"]}), 200


@goals_bp.route("/<id>/tasks", methods = ["GET"])
def get_tasks_for_goal(id):
    goal = get_goal_record_by_id(id)
    # tasks_info = [task.to_dict() for task in goal.tasks]
    tasks_info = []
    for task in goal.tasks:
        task_dict = {
            "id": task.id,
            "goal_id": goal.id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.is_complete
        }
        tasks_info.append(task_dict)

    return jsonify({
        "id":goal.id,
        "title": goal.title,
        "tasks": tasks_info}), 200
    
    
    
    # tasks_info = [task.to_dict() for task in goal.tasks]

    # request_body = request.get_json()




