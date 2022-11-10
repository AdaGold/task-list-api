from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task
from datetime import datetime
import requests
import os

SLACK_TOKEN = os.environ["Auth_token"]

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f" {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    
    if not all(["title" in request_body, "description" in request_body]):
        return {"details" : "Invalid data"}, 400

    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201


@tasks_bp.route("", methods=["GET"])
def get_tasks():

    sort_query = request.args.get("sort")
    if sort_query:
        if sort_query == "asc":
            tasks = Task.query.order_by(Task.title).all()
        elif sort_query == "desc":
            tasks = Task.query.order_by(Task.title.desc()).all()  
    else:
        tasks = Task.query.all()

    # task_response = []
    # for task in tasks:
    #     task_response.append(task.to_dict())
    task_response = [task.to_dict() for task in tasks]
    
    return jsonify(task_response)


@tasks_bp.route("/<id>", methods=["GET"])
def get_task(id):
    task = validate_model(Task, id)
    return {"task": task.to_dict()}, 200


@tasks_bp.route("/<id>", methods=["PUT"])
def update_task(id):
    task = validate_model(Task, id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {"task": task.to_dict()}, 200


@tasks_bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    task = validate_model(Task, id)

    db.session.delete(task)
    db.session.commit()

    return {"details": f'Task {task.id} "{task.title}" successfully deleted'}


@tasks_bp.route("/<id>/mark_complete", methods=["PATCH"])
def mark_complete(id):
    task = validate_model(Task, id)
    
    task.completed_at = datetime.utcnow()

    db.session.add(task)
    db.session.commit()

    url = "https://slack.com/api/chat.postMessage"
    data ={
        "channel": "task-notifications",
        "text": f"Someone just completed the task {task.title}"
    }

    headers ={
        "Authorization": f"{SLACK_TOKEN}"
        }
    
    post = requests.post(url=url, headers=headers, data=data)
    print(post.text)

    return {"task": task.to_dict()}, 200


@tasks_bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(id):
    task = validate_model(Task, id)
    
    task.completed_at = None

    db.session.commit()

    return {"task": task.to_dict()}, 200

#####################GOALS FOR TASKS##############
# @tasks_bp.route("/<task_id>/goals", methods=["GET"])
# def get_goals_for_task():
#     #goal = Goal.query.get(id)
#     tasks = [goal.to_dict() for task in goals.tasks]
#     return jsonify(tasks)
#     ...





