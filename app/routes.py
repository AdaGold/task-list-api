from app import db
from app.models.task import Task
from flask import Blueprint, request, jsonify

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["GET", "POST"])
def tasks():
    if request.method == "GET":
        sort_query = request.args.get("sort")
        if sort_query == "asc":
            tasks = Task.query.order_by(Task.title)
        elif sort_query == "desc":
            tasks = Task.query.order_by(Task.title.desc())
        else:
            task = Task.query.all()
        response_body = [task.to_dict() for task in tasks]
        return jsonify(response_body), 200

    elif request.method == "POST":
        request_body = request.get_json()

        if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
            return {"details": "Invalid data"}, 400

        task = Task.from_dict(request_body)

        db.session.add(task)
        db.session.commit()

        response_body={
            "task": task.to_dict()
        }

        return jsonify(response_body), 201

@tasks_bp.route("/<id>", methods=["GET", "PUT", "DELETE"])
def tasks_id(id):
    task = Task.query.get(id)
    if not task:
        return jsonify(None), 404

    if request.method == "GET":
        response_body = {
            "task": task.to_dict()
        }
        return response_body

    elif request.method == "PUT":
        request_body = request.get_json()
        task.title = request_body["title"]
        task.description = request_body["description"]

        db.session.commit()

        response_body = {
            "task": Task.query.get(id).to_dict()
        }

        return jsonify(response_body), 200

    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()

        response_body = {
            "details": f"Task {task.id} \"{task.title}\" successfully deleted"
        }

        return jsonify(response_body), 200
