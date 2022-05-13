from app import db
import os
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
from .routes_helper import error_message
from datetime import datetime
import requests

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def get_task_record_by_id(id):
    try:
        id = int(id)
    except:
        abort(make_response({"message":f"task {task.id} invalid"}, 400))
    
    task = Task.query.get(id)

    if not task:
        abort(make_response({"message":f"task {id} not found"}, 404))

    return task

def make_task_safely(data_dict):
    try:
        return Task.from_dict(data_dict)
    except KeyError as err:
        error_message("Invalid data", 400)

def marked_complete_bot_message(title):
    path = "https://slack.com/api/chat.postMessage"
    SLACK_API_KEY = os.environ.get('SLACK_API_KEY')

    query_params = {
        "channel": "task-list",
        "text":f"Someone just completed the task {title}"
    }

    call_headers = {"Authorization": f"Bearer {SLACK_API_KEY}" }

    api_call_response = requests.post(path, params=query_params, headers=call_headers)

    return api_call_response

@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    sort_param = request.args.get("sort")

    tasks = Task.query.all()

    if sort_param:
        if sort_param:
            titles = []
            for task in tasks:
                titles.append(task.title)
            if sort_param == "desc":
                sorted_titles = sorted(titles, reverse=True)
            elif sort_param == "asc":
                sorted_titles = sorted(titles)
            sorted_tasks = []
            for title in sorted_titles:
                for task in tasks:
                    if task.title == title:
                        sorted_tasks.append(task)
            tasks = sorted_tasks
        # elif sort_param == "desc":

    tasks_response = []
    for task in tasks:
        tasks_response.append(
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.is_complete,
                # "completed_at": task.completed_at
            }
        )
    return jsonify(tasks_response), 200



@tasks_bp.route("/<id>", methods=("GET",))
def read_task_by_id(id):
    task = get_task_record_by_id(id)
    if task.goal_id:
        response = {
        "id": task.id,
        "goal_id": task.goal_id,
        "title": task.title,
        "description": task.description,
        "is_complete": task.is_complete
    }
    else:
        response ={
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "is_complete": task.is_complete
    }
    return jsonify({"task":response}), 200

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    
    new_task = make_task_safely(request_body)

    db.session.add(new_task)
    db.session.commit()
    
    response = {"task":{
        "id":new_task.id,
        "title":new_task.title,
        "description":new_task.description,
        "is_complete":new_task.is_complete
    }}

    return make_response(jsonify(response), 201)

@tasks_bp.route("/<id>", methods=["PUT"])
def replace_task_by_id(id):
    task = get_task_record_by_id(id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    if "completed_at" in request_body.keys():
        task.completed_at = request_body["completed_at"]
        task.is_complete = True

    db.session.commit()

    response = {"task":{
        "id":task.id,
        "title":task.title,
        "description":task.description,
        "is_complete":task.is_complete
    }}

    return make_response(jsonify(response), 200)



@tasks_bp.route("/<id>/mark_complete", methods = ["PATCH"])
def mark_task_complete_by_id(id):
    task = get_task_record_by_id(id)
    task.is_complete = True
    task.completed_at = datetime.now()

    db.session.commit()

    response = {"task":{
        "id":task.id,
        "title":task.title,
        "description":task.description,
        "is_complete":task.is_complete
    }}

    marked_complete_bot_message(task.title)
    #Send bot message
    

    return make_response(jsonify(response), 200)

@tasks_bp.route("/<id>/mark_incomplete", methods = ["PATCH"])
def mark_task_incomplete_by_id(id):
    task = get_task_record_by_id(id)
    task.is_complete = False
    task.completed_at = None

    db.session.commit()

    response = {"task":{
        "id":task.id,
        "title":task.title,
        "description":task.description,
        "is_complete":task.is_complete
    }}

    return make_response(jsonify(response), 200)

@tasks_bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    task = get_task_record_by_id(id)

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({"details":f'Task {task.id} "{task.title}" successfully deleted'}))