from flask import Blueprint, request, make_response, jsonify, abort
from sqlalchemy import asc, desc
from app import db
from app.models.task import Task
from sqlalchemy.sql.functions import now
from app.models.goal import Goal

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


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
    # else:
    #     completed = False
    # task.completed_at = datetime.datetime.now()
    # I create a new dog and I want to put this in the data base (new object)
    db.session.add(new_task)
    
    # Need to have commit to see if I make some change to the database
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
    chosen_task = validated_task(task_id)

    return jsonify(
        {"task": {
        "id": chosen_task.task_id,
        "title": chosen_task.title,
        "description": chosen_task.description,
        "is_complete": False}})


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        return jsonify({"message":f"Task {task_id} is an invalid entry; must be a valid task id"}), 400


    task = Task.query.get(task_id)

    if task is None:
        return jsonify({"message":f"task {task_id} not found"}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({"details": f'Task {task_id} \"{task.title}\" successfully deleted'})


@tasks_bp.route('/<task_id>/mark_complete', methods=['PATCH'])
def mark_complete_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return "Error not found", 404
    
    task.completed_at = now()

    db.session.add(task)
    db.session.commit()

    return {"task": {
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": bool(task.completed_at)
    }}, 200

@tasks_bp.route('/<task_id>/mark_incomplete', methods=["PATCH"])
def mark_incomplete_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return "Error not found", 404

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
    task = Task.query.get(task_id)
    if task is None:
        return "Error not found", 404
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

"""Goal Model"""

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        return {"details": "Invalid data"}, 400

    new_goal = Goal(
        title=request_body["title"]
    )

    db.session.add(new_goal)
    db.session.commit()

    return {"goal": {
        "id": new_goal.goal_id,
        "title": new_goal.title
    }}, 201


def validated_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except ValueError:
        rsp = {"msg": f"Invalid id: {goal_id}"}
        abort(make_response(jsonify(rsp), 400))

    goal = Goal.query.get(goal_id)

    if goal is None:
        rsp = {"msg":f"Goal {goal_id} not found"}
        abort(make_response(jsonify(rsp), 404))

    return goal

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_goals(goal_id):
    chosen_goal = validated_goal(goal_id)

    return jsonify(
        {"goal": {
        "id": chosen_goal.goal_id,
        "title": chosen_goal.title,}}), 200

@goals_bp.route("", methods={"GET"})
def get_all_goal():
    goals = Goal.query.all()

    goals_response = []
    for goal in goals:
        goals_response.append({
            "id": goal.goal_id,
            "title": goal.title,
        })

    return jsonify(goals_response)

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    # goal = Goal.query.get(goal_id)
    goal = validated_goal(goal_id)
    
    request_body = request.get_json()
    
    goal.title = request_body["title"]

   
    db.session.commit()

    return {"goal": {
        "id": goal.goal_id,
        "title": goal.title,
    }}, 200

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except ValueError:
        return jsonify({"message":f"Goal {goal_id} is an invalid entry; must be a valid goal id"}), 400


    goal = Goal.query.get(goal_id)

    if goal is None:
        return jsonify({"message":f"task {goal_id} not found"}), 404

    db.session.delete(goal)
    db.session.commit()

    return jsonify({"details": f'Goal "{goal.title}" successfully deleted'})






