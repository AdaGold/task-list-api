from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, make_response, request, abort
from datetime import date, time, datetime
import requests

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message":f"task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message":f"task_id not found"}, 404))

    return task     

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"message":f"goal {goal_id} invalid" }, 400))
    
    goal = Goal.query.get(goal_id)

    if not goal:
        abort(make_response({"message":f"goal_id not found"}, 404))

    return goal 

def post_slack_message(message):
    path = "https://slack.com/api/chat.postMessage"
    API_KEY = "xoxb-4342317584466-4335756490678-gKLN3O9dpjHPgZ2aTJIxn5GX"
    query_params = {
        "channel": "task-notifications",
        "text": message
    }
    query_header = {"Authorization":f"Bearer {API_KEY}"}
    return requests.post(path,params = query_params, headers = query_header)


####TASK#####
@tasks_bp.route("", methods=["POST"])
def create_task():
    try:
        request_body = request.get_json()
        new_task = Task(title=request_body["title"],
                    description=request_body["description"])
    except KeyError as err:
        missing_field_response = {"details": "Invalid data"}
        return make_response(jsonify(missing_field_response), 400)

    db.session.add(new_task)
    db.session.commit()

    response = {"task":{
                "description": new_task.description,
                "id": new_task.task_id,
                "is_complete": False,
                "title": new_task.title 
            }}
    return make_response(jsonify(response), 201)
######GOAL#####
@goals_bp.route("", methods=["POST"])
def create_goal():
    try:
        request_body = request.get_json()
        new_goal = Goal(title=request_body["title"])
    except KeyError as err:
        missing_field_response = {"details": "Invalid data"}
        return make_response(jsonify(missing_field_response), 400)

    db.session.add(new_goal)
    db.session.commit()

    response = {"goal":{
                "id": new_goal.goal_id,
                "title": new_goal.title 
            }}
    return make_response(jsonify(response), 201)   
######TASK#####
@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    order_by = request.args.get("sort")
    if order_by == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif order_by == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(
            {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": False,
            }
        )
    return jsonify(tasks_response)
####GOAL####
@goals_bp.route("", methods=["GET"])
def read_all_goals():
    goals = Goal.query.all()
    goals_response = []
    for goal in goals:
        goals_response.append(
            {
                "id": goal.goal_id,
                "title": goal.title,
            }
        )
    return jsonify(goals_response)
#####TASK####   
@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_task(task_id)
    return {"task":{
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": False
                }
            }
#####GOAL#####
@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_goal(goal_id)
    return {"goal":{
                "id": goal.goal_id,
                "title": goal.title
                }
            }
#####TASK######   
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    response = {"task":{
                "description": task.description,
                "id": task.task_id,
                "is_complete": False,
                "title": task.title 
            }}
    return make_response(jsonify(response), 200)
####GOAL######
@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_task(goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    response = {"goal":{
                "id": goal.goal_id,
                "title": goal.title 
            }}
    return make_response(jsonify(response), 200)

#####TASK#######
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete_on_incompleted_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()
    task.completed_at = datetime.now() 
    if task.completed_at == None: 
        status = False
    else:
        status = True
    db.session.commit()
    post_slack_message(f"Someone just completed the task {task.title}.")
    response = {"task":{
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": status,
    }}
    return make_response(jsonify(response), 200)

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete_on_completed_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()
    task.completed_at = None
    if task.completed_at == None: 
        status = False
    else:
        status = True
    db.session.commit()
    response = {"task":{
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": status,
    }}
    return make_response(jsonify(response), 200)

    
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    response = {"details":(f"Task {task.task_id} \"{task.title}\" successfully deleted")}

    return make_response(jsonify(response), 200)

######GOAL#######
@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_task(goal_id)

    db.session.delete(goal)
    db.session.commit()

    response = {"details":(f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted")}

    return make_response(jsonify(response), 200)



    
    