
from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint,jsonify,abort,make_response,request
from sqlalchemy import desc
from sqlalchemy import asc
from datetime import datetime
import os
from dotenv import load_dotenv
import requests




tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
@tasks_bp.route("",methods=["GET"])
def handle_tasks_data():
    tasks_response = []
    title_query=request.args.get("title")

    sort_query=request.args.get("sort")
    if title_query:
        tasks=Task.query.filter_by(title=title_query)
    elif sort_query=="desc":
        tasks=Task.query.order_by(Task.title.desc()).all()
    elif sort_query=="asc":
        tasks=Task.query.order_by(Task.title.asc()).all()
    else:
        tasks=Task.query.all()
    
    for task in tasks:
        
        tasks_response.append({"id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete":False
        })
    return jsonify(tasks_response),200


def validate_task(id):
    try:
        task_id = int(id)
    except:
        abort(make_response({"message": f"Task {task_id} invalid"}, 400))
    task=Task.query.get(id)
    
    if not task:
        abort(make_response({"message":f"task {task_id} not found"}, 404))
    return task  


@tasks_bp.route("/<id>", methods=["GET"])

def read_one_task(id):
    
    task = validate_task(id)
    return jsonify({"task":task.to_dict()
        
    })

@tasks_bp.route("", methods=["POST"])

def create_task():
    request_body = request.get_json()
    try:
        new_task=Task.from_dict(request_body)
    except KeyError:
        if "title" not in request_body or "description" not in request_body:
            return make_response({"details": "Invalid data"},400)

    new_task =Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()
    
    return make_response(jsonify({"task":new_task.to_dict()}),201)
def slack_bot(message):
    PATH="https://slack.com/api/chat.postMessage"
    SLACK_API_KEY_BEARER=os.environ.get("API_KEY_BEARER")
    query_params={"channel":"task-notifications","text":message}
    requests.post(PATH,params=query_params,headers={"Authorization":SLACK_API_KEY_BEARER})



@tasks_bp.route("/<id>/mark_complete",methods=["PATCH"])
def mark_task_completeid(id):
    task = validate_task(id)
    task.completed_at=datetime.now()
    dict_rt=task.to_dict()
    db.session.commit()
    slack_bot(f"Someone just completed the task{task.title}")
    return make_response(jsonify({'task':dict_rt}),200)

@tasks_bp.route("/<id>/mark_incomplete",methods=["PATCH"])
def mark_task_incompleteid(id):
    task = validate_task(id)
    task.completed_at=None
    dict_rt=task.to_dict()
    db.session.commit()
    return make_response(jsonify({'task':dict_rt}),200)

@tasks_bp.route("/<id>", methods=["PUT"])
def update_task(id):
    task = validate_task(id)
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()
    return make_response(jsonify({"task":task.to_dict()}),200)

@tasks_bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    task = validate_task(id)

    db.session.delete(task)

    db.session.commit()
    

    return {"details": f'Task {task.id} "{task.title}" successfully deleted'}
    


