from flask import Blueprint, jsonify, make_response, request
from app import db
from app.models.task import Task
from datetime import datetime

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

"""
Want to make a helper function to return the dictionaries

def make_dict(json_body):
    if len(json_body) <= 1:
        return_dict.append({
        "id" : item.task_id,
        "title" : item.title,
        "description" : item.description,
        "is_complete" : item.is_complete
        }
        return return_dict

    else:
    return_list = []
    for item in json_body:
        return_list.append({
        "id" : item.task_id,
        "title" : item.title,
        "description" : item.description,
        "is_complete" : item.is_complete
        })

"""

@tasks_bp.route("", methods=["POST", "GET"])
def handle_tasks():
    if request.method == "GET":
        task = request.args.get("task")
        task_query = request.args.get("sort")
        #wave 2
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
        return {"task":
            {
            "id" : task.task_id,
            "title" : task.title,
            "description" : task.description,
            "is_complete" : task.is_complete
                }
            }, 200

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

#wave threeeeeeee

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def patch_it_up(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return jsonify(None), 404

    if request.method == "PATCH":
            task.completed_at = datetime.utcnow()
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