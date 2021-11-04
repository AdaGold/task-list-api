from flask import Blueprint, request, make_response, jsonify
from app import db
from app.models.task import Task
from app.models.goal import Goal
from datetime import datetime
import os
from dotenv import load_dotenv

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["POST","GET"])
def handle_tasks():
    if request.method=="POST":
        request_body = request.get_json()
        if "completed_at" not in request_body.keys() or "description" not in request_body.keys() or "title" not in request_body.keys():
            return make_response({"details": "Invalid data"}, 400) 
        else:
            new_task = Task(title=request_body["title"],
                        description=request_body["description"],
                        completed_at=request_body["completed_at"])
            db.session.add(new_task)
            db.session.commit()
            return make_response({"task": {
                    "id": new_task.task_id,
                    "title": new_task.title,
                    "description": new_task.description,
                    "is_complete": False if new_task.completed_at is None else True
                }}, 201)

    elif request.method=="GET":
        title_query = request.args.get('sort')
        if title_query=='desc':
            tasks = Task.query.order_by(Task.title.desc()).all()
        elif title_query=='asc':
            tasks = Task.query.order_by(Task.title).all()
        else:
            tasks=Task.query.all()
        tasks_response=[]
        for task in tasks:
            tasks_response.append({
                    "id": task.task_id,
                    "title": task.title,
                    "description": task.description,
                    "is_complete": False if task.completed_at is None else task.completed_at
                })
        return jsonify(tasks_response)

    
@tasks_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"])
def handle_a_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response('',404)

    elif request.method == "GET":
        if not task.goal_id:
            return {"task": { "id": task.task_id,
                        "title": task.title,
                        "description": task.description,
                        "is_complete": False if task.completed_at is None else task.completed_at  
                        }}
        else:
            return {"task": { "id": task.task_id,
                        "title": task.title,
                        "description": task.description,
                        "goal_id":task.goal_id,
                        "is_complete": False if task.completed_at is None else task.completed_at  
                        }}
                        
    elif request.method == "PUT":
        form_data = request.get_json()

        task.title = form_data["title"]
        task.description = form_data["description"]
        
        db.session.commit()

        

        return make_response({"task": { "id": task.task_id,
                                        "title": task.title,
                                        "description": task.description,
                                        "is_complete": False if task.completed_at is None else True  
                                        }})

    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return make_response({"details": f"Task {task.task_id} \"{task.title}\" successfully deleted"})

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):

    task = Task.query.get(task_id)
    if not task is None:
        task.completed_at = datetime.utcnow()
        db.session.commit()
        if task.title == "My Beautiful Task":
            
            client=slack.WebClient(token=os.getenv('SLACK_TOKEN'))
            client.chat_postMessage(
                    channel="slack-api-test-channel", 
                    text=f"Someone just completed the task {task.title}"
                )

        return make_response({"task": { "id": task.task_id,
                                                "title": task.title,
                                                "description": task.description,
                                                "is_complete": bool(task.completed_at)
                                                }}, 200)
        
    else:
        return make_response("",404)


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    task = Task.query.get(task_id)
    if not task is None:
        task.completed_at = None
        db.session.commit()

        return make_response({"task": { "id": task.task_id,
                                                "title": task.title,
                                                "description": task.description,
                                                "is_complete": bool(task.completed_at) #added bool
                                                }}, 200)
    else:
        return make_response("",404)


##### goals ######

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST","GET"])
def handle_goals():
    if request.method=="POST":
        request_body = request.get_json()
        if "title" not in request_body.keys():
            return make_response({"details": "Invalid data"}, 400) 
        else:
            new_goal = Goal(title=request_body["title"])
            db.session.add(new_goal)
            db.session.commit()
            
            return make_response({"goal": {
                    "id": new_goal.goal_id,
                    "title": new_goal.title
                }}, 201)

    elif request.method=="GET":
        title_query = request.args.get('sort')
        if title_query=='desc':
            goals = Goal.query.order_by(Goal.title.desc()).all()
        elif title_query=='asc':
            goals = Goal.query.order_by(Goal.title).all()
        else:
            goals=Goal.query.all()
        goals_response=[]
        for goal in goals:
            goals_response.append({
                    "id": goal.goal_id,
                    "title": goal.title
                })
        return jsonify(goals_response)

    
@goals_bp.route("/<goal_id>", methods=["GET", "PUT", "DELETE"])
def handle_a_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal is None:
        return make_response('',404)

    elif request.method == "GET":
        return {"goal": { "id": goal.goal_id,
                        "title": goal.title
                        }}
                        
    elif request.method == "PUT":
        form_data = request.get_json()

        goal.title = form_data["title"]

        db.session.commit()

        return make_response({"goal": { "id": goal.goal_id,
                                        "title": goal.title
                                        }})

    elif request.method == "DELETE":
        db.session.delete(goal)
        db.session.commit()
        return make_response({"details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"})

@goals_bp.route("/<goal_id>/tasks", methods=["POST","GET"])
def handle_tasks_in_goals(goal_id):
    goal = Goal.query.get(goal_id)
    if goal is None:
        return make_response("", 404)

    if request.method == "POST":
        request_body = request.get_json()
        three_task_ids=request_body["task_ids"]
        goal_tasks=[]

        for task_id in three_task_ids:
            goal_task = Task.query.get(task_id)
            goal_tasks.append(goal_task)
            goal_task.goal=goal
            db.session.commit()
        return make_response({"id": goal.goal_id, "task_ids": three_task_ids})
    
    elif request.method=="GET":

        tasks_response = []
        for task in goal.tasks:
            tasks_response.append({
            "id": task.task_id,
            "goal_id": task.goal_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
            }
        )
        print(tasks_response)
        return make_response({"id": goal.goal_id,
  "title": goal.title,
  "tasks": tasks_response}, 200)
                        
