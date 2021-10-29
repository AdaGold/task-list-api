from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, request
from sqlalchemy import asc, desc
from datetime import date

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["GET", "POST"])
def handle_tasks():
    if request.method == "GET":
        sort_query = request.args.get("sort")
        if sort_query:
            #potential refactor: order by default orders category by asc, so I could remove asc() and just say order_by(Task.title) ?
            if sort_query == "asc":
                tasks = Task.query.order_by(asc(Task.title))
            else:
                tasks = Task.query.order_by(desc(Task.title))
        else:
            tasks = Task.query.all()

        tasks_response = []
        for task in tasks:
            tasks_response.append({
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)
            })

        return jsonify(tasks_response)

    elif request.method == "POST":
        request_body = request.get_json()

        try:
            new_task = Task(title=request_body["title"],
                            description=request_body["description"], completed_at=request_body["completed_at"])

            db.session.add(new_task)
            db.session.commit()

            response = {
                "task": {
                    "id": new_task.id,
                    "title": new_task.title,
                    "description": new_task.description,
                    "is_complete": bool(new_task.completed_at)
                }
            }

            return jsonify(response), 201
        except KeyError:
            return jsonify({"details": "Invalid data"}), 400


@tasks_bp.route("/<id>", methods=["GET", "PUT", "DELETE"])
def handle_task(id):
    task = Task.query.get(id)
    if task is None:
        return jsonify(None), 404

    if request.method == "GET":
        return {
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)
            }
        }

    elif request.method == "PUT":
        request_body = request.get_json()

        task.title = request_body["title"]
        task.description = request_body["description"]

        db.session.commit()

        response = {
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)
            }
        }
        return jsonify(response)

    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()

        response = {
            'details': f'Task {task.id} "{task.title}" successfully deleted'
        }
        return jsonify(response), 200

@tasks_bp.route("/<id>/mark_complete", methods=["PATCH"])
def update_task_completed(id):
    task = Task.query.get(id)
    if task is None:
        return jsonify(None), 404

    task.completed_at = date.today()
    db.session.commit()

    response = {
        "task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        }
    }
    return jsonify(response), 200

#refactor these two routes to be one /<id?/<mark completion> 

@tasks_bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def update_task_not_completed(id):
    task = Task.query.get(id)
    if task is None:
        return jsonify(None), 404

    task.completed_at = None
    db.session.commit()

    response = {
        "task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        }
    }
    return jsonify(response), 200

    

# potential refactors:
    # formating of the resopnse {task :  {}} repeated throughout, as well as {details: "fka;df"}
    # potential fixture or helper function that formats :
        # {
        #     "id": task.id,
        #     "title": task.title,
        #     "description": task.description,
        #     "is_complete": bool(task.completed_at)
        # }
