from app import db
from app.models.goal import Goal
from flask import Blueprint,jsonify,abort,make_response,request
from sqlalchemy import desc
from sqlalchemy import asc
from datetime import datetime
import os
from dotenv import load_dotenv
import requests


goals_bp=Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("",methods=["GET"])
def handle_goals_data():
    goals_response = []
    title_query=request.args.get("title")

    sort_query=request.args.get("sort")
    if title_query:
        goals=Goal.query.filter_by(goal_title=title_query)
    elif sort_query=="desc":
        goals=Goal.query.order_by(Goal.goal_title.desc()).all()
    elif sort_query=="asc":
        goals=Goal.query.order_by(Goal.goal_title.asc()).all()
    else:
        goals=Goal.query.all()
    
    for goal in goals:
        
        goals_response.append({
            "id": goal.goal_id,
            "title": goal.goal_title,
            
        })
    return jsonify(goals_response),200

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"message": f"Goal {goal_id} invalid"}, 400))
    goal=Goal.query.get(id)
    
    if not goal:
        abort(make_response({"message":f"task {goal_id} not found"}, 404))
    return goal 


@goals_bp.route("/<id>", methods=["GET"])

def read_one_goal(id):
    
    goal = validate_goal(id)
    return jsonify({"task":{
        "id": goal.goal_id,
        "title": goal.goal_title,
        
    }})

@goals_bp.route("", methods=["POST"])

def create_goal():
    request_body = request.get_json()
    try:
        new_goal=Goal.from_dictg(request_body)
    except KeyError:
        if "title" not in request_body:
            return make_response({"details": "Invalid data"},400)

    new_goal =Goal.from_dictg(request_body)

    db.session.add(new_goal)
    db.session.commit()
    
    return make_response(jsonify({"goal":new_goal.to_dictg()}),201)

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()
    goal.goal_title = request_body["title"]
    db.session.commit()
    return make_response(jsonify({"goal":goal.to_dictg()}),200)

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal= validate_goal(goal_id)

    db.session.delete(goal)

    db.session.commit()
    

    return {"details": f'Goal {goal.goal_id} "{goal.goal_title}" successfully deleted'}