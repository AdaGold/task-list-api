from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, make_response, request, abort
from datetime import date
import requests, os

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def validate_task(task_id):  
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message":f"task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message":f"task {task_id} not found"}, 404))

    return task

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
    
    return ({"task":{
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": False
        }}, 201)


@tasks_bp.route("", methods=["GET"])
def read_all_tasks():  # sourcery skip: list-comprehension

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

    tasks_response = []
    for task in tasks:
        tasks_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        })

    return jsonify(tasks_response)


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)
    return {"task":{
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        }}

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]
    
    db.session.commit()

    return {"task":{
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        }}

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)
    
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

    task = validate_task(task_id) 

    if complete == "mark_complete":     
        task.completed_at = date.today()
        is_complete = True

    elif complete == "mark_incomplete":
        task.completed_at = None
        is_complete = False
        
    db.session.commit()

    task_response = {"task":{
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": is_complete
        }}
    if is_complete == True:
        make_slack_post(task.title)
    
    return make_response(task_response)


# GOAL STARTS HERE

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

def validate_goal(goal_id):  
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"message":f"goal {goal_id} invalid"}, 400))

    goal = Goal.query.get(goal_id)

    if not goal:
        abort(make_response({"message":f"goal {goal_id} not found"}, 404))

    return goal

@goals_bp.route("", methods=["POST"])
def create_goal():

    request_body = request.get_json()
    
    if "title" not in request_body:
            abort(make_response({"details": "Invalid data" }, 400))

    new_goal = Goal(
        title=request_body["title"],
        )

    db.session.add(new_goal)
    db.session.commit()
    
    return ({"goal":{
            "id": new_goal.goal_id,
            "title": new_goal.title
        }}, 201)

@goals_bp.route("", methods=["GET"])
def get_all_goals():  

    goals = Goal.query.all()

    goals_response = []
    for goal in goals:
        goals_response.append({
            "id": goal.goal_id,
            "title": goal.title
        })

    return jsonify(goals_response)

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)
    return {"goal":{
            "id": goal.goal_id,
            "title": goal.title,
        }}


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goal(goal_id)
    
    db.session.delete(goal)
    db.session.commit()

    return ({
    "details": f'Goal {goal_id} "{goal.title}" successfully deleted'
    }, 200)

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()
    goal.title = request_body["title"]
    
    db.session.commit()

    return {"goal": {
            "id": goal.goal_id,
            "title": goal.title   
        }}