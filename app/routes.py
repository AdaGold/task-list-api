from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task
from sqlalchemy import asc, desc
from datetime import date, time, datetime
import json
import requests
import os
from dotenv import load_dotenv
from app.models.goal import Goal

load_dotenv()

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

## Validate Model ##
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{model_id} is not a valid type ({type(model_id)}). Must be an integer)"}, 400))

    model = cls.query.get(model_id)
    
    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} does not exist"}, 404))
        
    return model
        
## CREATE
@task_bp.route("", methods=['POST'])
def create_task():
    request_body = request.get_json()
    
    if not request_body.get('title') or not request_body.get('description'):
        abort(make_response({"details": "Invalid data"}, 400))
        
    task = Task.from_dict(request_body)
    
    db.session.add(task)
    db.session.commit()
    return {"task": task.to_dict()}, 201

## READ - ALL
@task_bp.route("", methods=["GET"])
def read_all_tasks():
    task_query = request.args.get("sort")
    
    if task_query == 'asc':
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif task_query == 'desc':
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()

    tasks_response = []
    
    for task in tasks:
        task_dict = task.to_dict()
        tasks_response.append(task_dict)
    
    return jsonify(tasks_response), 200

## READ - ONE
@task_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id)

    return {"task": task.to_dict()}, 200

## UPDATE - PUT
@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()
    
    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()
    
    return jsonify({"task": task.to_dict()}), 200

## UPDATE - INCOMPLETE
@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def update_task_incomplete(task_id):
    task = validate_model(Task, task_id)
    
    task.completed_at = None
    
    db.session.commit()

    return {"task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "is_complete": False}
            }     
    
# ## UPDATE - COMPLETE
# @task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
# def patch_task_complete(task_id):
#     task = validate_model(Task, task_id)
    
#     task.completed_at = datetime.today()

#     db.session.commit()
#     return {'task': task.to_dict()}, 200

## UPDATE - COMPLETE - SLACK
@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def update_task_complete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = datetime.today()
    
    # if headers != {'Authorization': f"Bearer {os.environ.get('SLACKBOT_API_KEY')}"}:
    #     return {
    #             "ok": False,
    #             "error": "invalid_auth"
    #         }, 400 .abort(status)

    channel_id = 'task-notifications'
    url = 'https://slack.com/api/chat.postMessage'
    
    params = {'channel': channel_id, 'text': f"Someone just completed the task {task.title}."}
    
    headers = {'Authorization': f"Bearer {os.environ.get('SLACKBOT_API_KEY')}"}
    requests.post(url=url, params=params, headers=headers)

    db.session.commit()
    return jsonify({'task': task.to_dict()}), 200

## DELETE
@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)
    
    db.session.delete(task)
    db.session.commit()
    
    return {
        "details": f'Task {task_id} "{task.title}" successfully deleted'
    }


############## GOAL ROUTES #################


## CREATE
@goal_bp.route("", methods=['POST'])
def create_goal():
    request_body = request.get_json()
    
    if not request_body.get('title'):
        abort(make_response({"details": "Invalid data"}, 400))
        
    # goal = Goal.from_dict(request_body)
    goal = Goal(title=request_body["title"])
    
    db.session.add(goal)
    db.session.commit()
    return jsonify({"goal": goal.to_dict()}), 201

## READ - ALL
@goal_bp.route("", methods=["GET"])
def read_all_goals():
    goals = Goal.query.all()
    goals_response = []
    
    for goal in goals:
        goals_response.append(goal.to_dict())
    
    return jsonify(goals_response), 200

## READ - ONE
@goal_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return {"goal": goal.to_dict()}, 200

## UPDATE - PUT
@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    
    goal.title = request_body["title"]

    db.session.add(goal)
    db.session.commit()
    
    return {"goal": goal.to_dict()}, 200


## DELETE
@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    db.session.delete(goal)
    db.session.commit()
    
    return {
        "details": f'Goal {goal_id} "{goal.title}" successfully deleted'
    }
    
############## TASK GOAL RELATIONSHIP ROUTES #################
    
## CREATE - post task ids to one goal id
@goal_bp.route("/<goal_id>/tasks", methods = ["POST"])
def add_task_ids_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    new_task_list = request_body["task_ids"]
    for task_id in new_task_list:
        task = validate_model(Task, task_id)
        task.goal = goal

        db.session.add(task)
        db.session.commit()

    return jsonify({"id": goal.goal_id, "task_ids": new_task_list}), 200


## READ - tasks by goal
@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def read_tasks_by_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    tasks_response = []

    response_body = {
        "id": goal.goal_id,
        "title": f"{goal.title}",
        "tasks": tasks_response
    }
    
    for task in goal.tasks: 
        response_body["tasks"].append(task.id_to_dict())

    return jsonify(response_body), 200