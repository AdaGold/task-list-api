"""
Something went very, very wrong and I had to scrap my original repository, 
start over and copy paste my code in. Hence, the lack of commits. 
I was beginning the deployment stage and accidently deleted the origin remote. 
This lead me down a very dark path, trying different git commands that I didnt fully understand. 
It was chaos.

Anyways,
I didn't have time to do docstrings.
Also, I experimented with doubling up the route decorators since the functions were 
pretty much the same for Task & Goals.
Not sure if this is a no no in real life, or if there is a better way to do it. Let me know!
"""


from flask import Blueprint, jsonify, request, abort, g
from app import db
from app.models.task import Task
from app.models.goal import Goal
from datetime import datetime
import requests
import os

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


def slack_bot(text):

    SLACK_KEY = os.environ.get("SLACK_KEY")
    req_body = {"channel": "task-notifications", "text": text}
    headers = {"Authorization": f"Bearer {SLACK_KEY}"}
    path = "https://slack.com/api/chat.postMessage"

    requests.post(path, json=req_body, headers=headers)


def validate(model, id):

    try:
        id = int(id)
    except ValueError:
        abort(400)
    return model.query.get_or_404(id)


def sort(model):

    sort = request.args.get("sort")
    if sort == "asc":
        model = model.query.order_by(model.title.asc())
    elif sort == "desc":
        model = model.query.order_by(model.title.desc())

    return model


@goals_bp.before_request
@tasks_bp.before_request
def get_model():

    bps = {"tasks": (Task, "task"), "goals": (Goal, "goal")}
    g.model, g.name = bps[request.blueprint]


@goals_bp.route("", methods=["GET"])
@tasks_bp.route("", methods=["GET"])
def get_all():

    model = g.model
    if "sort" in request.args:
        models = sort(model)
    else:
        models = model.query.all()

    return jsonify([model.to_dict() for model in models])


@goals_bp.route("/<id>", methods=["GET"])
@tasks_bp.route("/<id>", methods=["GET"])
def get_one(id):

    model, name = g.model, g.name
    model = validate(model, id)

    return {f"{name}": model.to_dict()}


@goals_bp.route("", methods=["POST"])
@tasks_bp.route("", methods=["POST"])
def create():

    model, name = g.model, g.name
    request_body = request.get_json()

    try:
        if model == Task:
            new_entry = model(
                title=request_body["title"],
                description=request_body["description"],
                completed_at=request_body["completed_at"],
            )
        elif model == Goal:
            new_entry = model(title=request_body["title"])

    except:
        return {"details": "Invalid data"}, 400

    db.session.add(new_entry)
    db.session.commit()

    return {f"{name}": new_entry.to_dict()}, 201


@goals_bp.route("/<id>", methods=["PUT"])
@tasks_bp.route("/<id>", methods=["PUT"])
def update_one(id):
    model, name = g.model, g.name
    model = validate(model, id)
    request_body = request.get_json()

    model.update(request_body)

    db.session.commit()
    return {f"{name}": model.to_dict()}


@goals_bp.route("/<id>", methods=["DELETE"])
@tasks_bp.route("/<id>", methods=["DELETE"])
def delete_one(id):

    model, name = g.model, g.name
    model = validate(model, id)

    db.session.delete(model)
    db.session.commit()

    return {
        "details": f'{name.capitalize()} {model.id} "{model.title}" successfully deleted'
    }


@tasks_bp.route("/<id>/mark_complete", methods=["PATCH"])
def mark_task_complete(id):

    task = validate(Task, id)
    text = f"Someone just completed the task {task.title}"
    slack_bot(text)

    task.completed_at = datetime.now()
    db.session.commit()

    return {"task": task.to_dict()}


@tasks_bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(id):

    task = validate(Task, id)
    task.completed_at = None
    db.session.commit()

    return {"task": task.to_dict()}


@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_tasks_to_goal(goal_id):
    goal = validate(Goal, goal_id)
    request_body = request.get_json()

    try:
        goal.tasks = [validate(Task, task_id) for task_id in request_body["task_ids"]]
    except:
        return {"details": "Invalid data"}, 400

    return {"id": goal.id, "task_ids": [task.id for task in goal.tasks]}


@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_by_goal(goal_id):
    goal = validate(Goal, goal_id)
    return goal.to_dict(has_tasks=True)
