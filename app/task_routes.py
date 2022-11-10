from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, make_response, request, abort
from datetime import date
import requests, os
from .routes_helper import validate_model

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():

    request_body = request.get_json()
    
    attributes = ["title", "description"]

    for attribute in attributes:
        if attribute not in request_body or len(request_body[attribute]) == 0:
            abort(make_response({"details": "Invalid data" }, 400))

    new_task = Task(
        title=request_body["title"],
        description=request_body["description"],
        )

    db.session.add(new_task)
    db.session.commit()
    
    return ({"task": new_task.to_dict()}, 201)


@tasks_bp.route("", methods=["GET"])
def read_all_tasks():  

    task_query = request.args.get("task")
    sort_at_query = request.args.get("sort")
    if task_query:
        tasks = Task.query.filter_by(title=task_query)
    elif sort_at_query == "asc":
        tasks = Task.query.order_by(Task.title)
    elif sort_at_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    tasks_response = [task.to_dict() for task in tasks]
    
    return jsonify(tasks_response)


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    return {"task": task.to_dict()}
    
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    
    task = validate_model(Task, task_id)
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]
    
    db.session.commit()

    return {"task": task.to_dict()}


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)
    
    db.session.delete(task)
    db.session.commit()

    return ({
    "details": f'Task {task_id} "{task.title}" successfully deleted'
    }, 200)


def make_slack_post(title):
    URL = "https://slack.com/api/chat.postMessage"
    
    params={"channel":"slack-bot-test-channel" ,
    "text": f"Someone just completed the task {title}"}
    
    headers = {"Authorization": os.environ.get('SLACK_KEY')}

    return requests.post(URL, params= params, headers=headers)

@tasks_bp.route("/<task_id>/<complete>", methods=["PATCH"])
def patch_complete_task(task_id, complete):

    task = validate_model(Task, task_id)

    if complete == "mark_complete":     
        task.completed_at = date.today()
        is_complete = True

    elif complete == "mark_incomplete":
        task.completed_at = None
        is_complete = False
        
    db.session.commit()

    task_response = {"task": task.to_dict()}
    if is_complete == True:
        make_slack_post(task.title)
    
    return make_response(task_response)




