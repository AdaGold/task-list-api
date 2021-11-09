from flask import Blueprint, jsonify, make_response, request
from app import db
from app.models.task import Task
from app.models.goal import Goal
from datetime import datetime
import os
import requests
from dotenv import load_dotenv
load_dotenv()

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@tasks_bp.route("", methods=["POST", "GET"])
def handle_tasks():
    if request.method == "GET":
        task = request.args.get("task")
        task_query = request.args.get("sort")

        if task_query:
            if task_query == "asc":
                tasks = Task.query.order_by(Task.title.asc())
            elif task_query == "desc":
                tasks = Task.query.order_by(Task.title.desc())
        else:
            tasks = Task.query.all()
        tasks_response = []
        for task in tasks:
            tasks_response.append(
                {
                    "id" : task.task_id,
                    "title" : task.title,
                    "description" : task.description,
                    "is_complete" : task.is_complete
                }
            )
        
        return jsonify(tasks_response), 200

    elif request.method == "POST":
        request_body = request.get_json()

        #replace with try/except
        #this is my guard clause
        if (("title" not in request_body.keys()) or 
        ("description" not in request_body.keys()) or
        ("completed_at" not in request_body.keys())):
            return jsonify(
                {"details": "Invalid data"}
            ), 400

        if not request_body["completed_at"]:
            new_task = Task(title=request_body["title"],
                            description=request_body["description"],
                            completed_at=request_body["completed_at"],
                            )
            db.session.add(new_task)
            db.session.commit()


            return jsonify({"task":
                {
                "id" : new_task.task_id,
                "title" : new_task.title,
                "description" : new_task.description,
                "is_complete" : new_task.is_complete
                    }
                }), 201

        elif request_body["completed_at"]:
            new_task = Task(title=request_body["title"],
                            description=request_body["description"],
                            completed_at=request_body["completed_at"],
                            is_complete=True
                            )
            db.session.add(new_task)
            db.session.commit()


            return jsonify({"task":
                {
                "id" : new_task.task_id,
                "title" : new_task.title,
                "description" : new_task.description,
                "is_complete" : new_task.is_complete
                    }
                }), 201


@tasks_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"])
def handle_task(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return jsonify(None), 404

    if request.method == "GET":
        
        return_dict = {"task":
            {
            "id" : task.task_id,
            "title" : task.title,
            "description" : task.description,
            "is_complete" : task.is_complete
                }
            }

        if task.goal_id:
            return_dict["task"]["goal_id"] = task.goal_id

        return return_dict, 200

    elif request.method == "PUT":
        request_body = request.get_json()

        if not task.completed_at:
        
            task.title = request_body["title"]
            task.description = request_body["description"]

            db.session.commit()

        elif task.completed_at:
            task.title = request_body["title"]
            task.description = request_body["description"]
            task.is_complete = True

            db.session.commit()

        return jsonify(
                {
                "task":
                {
                "id" : task.task_id,
                "title" : task.title,
                "description" : task.description,
                "is_complete" : task.is_complete
                    }
                }
                ), 200



    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return jsonify(
            {
                'details': (f'Task {task.task_id} \"{task.title}\" successfully deleted')
            }

        ), 200


PATH = "https://slack.com/api/chat.postMessage"
API_KEY = os.environ.get("SLACK_KEY")

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def patch_it_up(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return jsonify(None), 404

    if request.method == "PATCH":
        task.completed_at = datetime.utcnow()
        task.is_complete = True
        db.session.commit()

        #we put the auth here
        header = {"authorization" : f"Bearer {API_KEY}"
        }
        post_body = {"channel" : "slack-api-test-channel",
        "text": f"Someone just completed the task {task.title}"
        }
        
        requests.post(PATH, headers=header, json=post_body)


        return jsonify(
                {
                "task":
                {
                "id" : task.task_id,
                "title" : task.title,
                "description" : task.description,
                "is_complete" : task.is_complete
                }
                }
                ), 200


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def patch_it_down(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return jsonify(None), 404

    if request.method == "PATCH":
        task.completed_at = None
        task.is_complete = False
        db.session.commit()


        return jsonify(
            {
            "task":
            {
            "id" : task.task_id,
            "title" : task.title,
            "description" : task.description,
            "is_complete" : task.is_complete
            }
            }
            ), 200



@goals_bp.route("", methods=["GET", "POST"])
def handle_goals():

    request_body = request.get_json()
    goals = Goal.query.all()

    if request.method == "GET":
 
        goals_response = []
        for goal in goals:
            goals_response.append(
                {
                    "id" : goal.goal_id,
                    "title" : goal.title
                }
            )

        return jsonify(goals_response), 200

    elif request.method == "POST":
        request_body = request.get_json()

        if "title" not in request_body:
            return jsonify(
                {
                "details": "Invalid data"
                }
                ), 400

        new_goal = Goal(title=request_body["title"])

        db.session.add(new_goal)
        db.session.commit()

        return {
                "goal": { "id": new_goal.goal_id,
                "title": new_goal.title
                }
                }, 201
        

@goals_bp.route("/<goal_id>", methods=["GET", "PUT", "DELETE"])
def handle_goal(goal_id):
    goal = Goal.query.get(goal_id)

    if goal is None:
        return jsonify(None), 404

    if request.method == "GET":
        return {"goal":
            {
            "id" : goal.goal_id,
            "title" : goal.title
                }
            }, 200

    elif request.method == "PUT":
        request_body = request.get_json()

        goal.title = request_body["title"]

        db.session.commit()

        return {
                "goal": {"id": goal.goal_id, "title": goal.title
                }
                }, 200
    elif request.method == "DELETE":
        db.session.delete(goal)
        db.session.commit()
        return jsonify(
            {
                'details': (f'Goal {goal.goal_id} \"{goal.title}\" successfully deleted')
            }

        ), 200

@goals_bp.route("/<goal_id>/tasks", methods=["POST", "GET"])
def goals_and_tasks(goal_id):
    goal = Goal.query.get(goal_id)
    request_body = request.get_json()

    if not goal:
        return jsonify(None), 404

    if request.method == "POST":
        
        the_list = []
        for num in request_body["task_ids"]:
            the_task = Task.query.get(num)
            the_list.append(the_task)
        
        print(the_list)
        goal.tasks = the_list

        db.session.commit()

        task_id_list = []
        for task in goal.tasks:
            task_id_list.append(task.task_id)
            print(task_id_list)

        return jsonify({
            "id" : goal.goal_id,
            "task_ids" : task_id_list
        }), 200
    
    if request.method == "GET":

        task_list = []
        for task in goal.tasks:
            task_list.append({
                "id": task.task_id,
                "goal_id": task.goal_id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.is_complete
            }
            )

        return jsonify({
            "id" : goal.goal_id,
            "title" : goal.title,
            "tasks" : task_list
        }), 200
