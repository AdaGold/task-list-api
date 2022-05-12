from app import db
from app.models.goal import Goal
from flask import Blueprint, jsonify, abort, make_response, request
from .routes_helper import error_message
from datetime import datetime
import requests

BOT_TOKEN = "xoxb-3517483621795-3514864472709-eftmGUbZpBrItU54XIpAnwQo"

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

def get_goal_record_by_id(id):
    try:
        id = int(id)
    except:
        abort(make_response({"message":f"goal {goal.id} invalid"}, 400))
    
    goal = Goal.query.get(id)

    if not goal:
        abort(make_response({"message":f"goal {id} not found"}, 404))

    return goal

def make_goal_safely(data_dict):
    try:
        return Goal.from_dict(data_dict)
    except KeyError as err:
        error_message("Invalid data", 400)

def marked_complete_bot_message(title):
    path = "https://slack.com/api/chat.postMessage"

    query_params = {
        "channel": "goal-list",
        "text":f"Someone just completed the goal {title}"
    }

    call_headers = {"Authorization": "Bearer xoxb-3517483621795-3514864472709-eftmGUbZpBrItU54XIpAnwQo" }

    api_call_response = requests.post(path, params=query_params, headers=call_headers)

    return api_call_response

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



# IMDB_API_KEY = "39aa0fecd969cfc4feb999c6fd8e6c8c"

# def generate_token():
#     path = "https://api.themoviedb.org/3/authentication/token/new"

#     query_params = {
#         "api_key": IMDB_API_KEY
#     }

#     response = requests.get(path, params=query_params)

#     response_body = response.json()
#     response_body
#     request_token = response_body["request_token"]
#     return request_token

@goals_bp.route("/<id>/mark_complete", methods = ["PATCH"])
def mark_goal_complete_by_id(id):
    goal = get_goal_record_by_id(id)
    # goal.is_complete = True
    # goal.completed_at = datetime.now()

    db.session.commit()

    response = {"goal":{
        "id":goal.id,
        "title":goal.title
    }}

    marked_complete_bot_message(goal.title)
    #Send bot message
    

    return make_response(jsonify(response), 200)

@goals_bp.route("/<id>/mark_incomplete", methods = ["PATCH"])
def mark_goal_incomplete_by_id(id):
    goal = get_goal_record_by_id(id)
    # goal.is_complete = False
    # goal.completed_at = None

    db.session.commit()

    response = {"goal":{
        "id":goal.id,
        "title":goal.title
    }}

    return make_response(jsonify(response), 200)

@goals_bp.route("/<id>", methods=["DELETE"])
def delete_goal(id):
    goal = get_goal_record_by_id(id)

    db.session.delete(goal)
    db.session.commit()

    return make_response(jsonify({"details":f'goal {goal.id} "{goal.title}" successfully deleted'}))