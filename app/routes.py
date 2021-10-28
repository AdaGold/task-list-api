from flask import Blueprint, jsonify, make_response, request
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST", "GET"])
def handle_tasks():
    if request.method == "GET":
        task = request.args.get("task")
        if task:
            tasks = Task.query.filter_by(task=task)
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

        

        new_task = Task(title=request_body["title"],
                        description=request_body["description"],
                        completed_at=request_body["completed_at"]
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

        task.title = request_body["title"]
        task.description = request_body["description"]

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


