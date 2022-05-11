
from flask import Blueprint, request, make_response, jsonify, abort
from sqlalchemy import asc, desc
from app import db
from app.models.task import Task
from sqlalchemy.sql.functions import now
import requests, os


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    #the client make some request
    #request body is a dictionary that pull a request from json
    #convert the json object into python data
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        return make_response({'details': "Invalid data"}, 400)

    # whatever in the request body
    new_task = Task(
        title = request_body["title"],
        description = request_body["description"]
    )
    if "completed_at" in request_body:
        new_task.completed_at = request_body["completed_at"]
    # I create a new dog and I want to put this in the data base (new object)
    db.session.add(new_task)
    db.session.commit()

    return {"task": {
        "id": new_task.task_id,
        "title": new_task.title, 
        "description": new_task.description, 
        "is_complete": bool(new_task.completed_at)}}, 201


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    task_query = request.args

    if "sort" in task_query:
        if task_query["sort"] == "desc":
            tasks = Task.query.order_by(desc(Task.title)).all()
        else:
            tasks = Task.query.order_by(asc(Task.title)).all()
    else:
        # To get all the task from the table
         tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append({
            "id": task.task_id,
            "description": task.description,
            "title": task.title,
            "is_complete": False
        })

    return jsonify(tasks_response)

def validated_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        rsp = {"msg": f"Invalid id: {task_id}"}
        abort(make_response(jsonify(rsp), 400))

    task = Task.query.get(task_id)

    if task is None:
        rsp = {"message":f"Task {task_id} not found"}
        abort(make_response(jsonify(rsp), 404))

    return task


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validated_task(task_id)

    return jsonify(
        {"task": task.to_dict()})


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task = validated_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({"details": f'Task {task_id} \"{task.title}\" successfully deleted'})


@tasks_bp.route('/<task_id>/mark_complete', methods=['PATCH'])
def mark_complete_task(task_id):
    task = validated_task(task_id)
    task.completed_at = now()

    db.session.add(task)
    db.session.commit()

    SLACK_API_URL = "https://slack.com/api/chat.postMessage"
    SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")

    query_params = {
            "channel": "task_notifications",
            "text": f"Someone just completed the task {task.title}"
        }

    headers = {"Authorization": SLACK_BOT_TOKEN}

    url = requests.post(SLACK_API_URL, headers=headers, params=query_params)


    return {"task": {
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": bool(task.completed_at)
    }}, 200

@tasks_bp.route('/<task_id>/mark_incomplete', methods=["PATCH"])
def mark_incomplete_task(task_id):
    task = validated_task(task_id)
    task.completed_at = None

    db.session.add(task)
    db.session.commit()
    

    return {"task": {
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": bool(task.completed_at)
    }}, 200


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task_complete_date(task_id):
    task = validated_task(task_id)
    request_body = request.get_json()
    
    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.add(task)
    db.session.commit()

    return {"task": {
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": bool(task.completed_at)
    }}, 200



