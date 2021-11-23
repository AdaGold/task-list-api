from flask import Blueprint, jsonify
from flask.globals import request 
from app.models.task import Task
from app import db


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["GET","POST"])
def handle_tasks():
    if request.method == "GET":
        sorting_task = request.args.get('sort')
        list = None
        if sorting_task == "desc":
            list = Task.query.order_by(Task.title.desc())
        elif sorting_task == "asc":
            list = Task.query.order_by(Task.title.asc()) 
        else:
            list = Task.query.all()

        tasks_response = []
        for task in list:
            tasks_response.append({
            "id":task.task_id,
            "title": task.title,
            "description":task.description,
            "is_complete":task.completed_at
            })
        for task in tasks_response:
            if task["is_complete"]:
                task["is_complete"] = True
            else: 
                task["is_complete"] = False

        return jsonify(tasks_response),200

    elif request.method == "POST":
        request_body = request.get_json()
        new_task = Task(title=request_body["title"], description=request_body["description"], completed_at=request_body["completed_at"])
        
     
        db.session.add(new_task)
        db.session.commit()

        return jsonify({
            "task":{
                "task_id": new_task.task_id,

                }
        })

# @tasks_bp.route('/<task_id>', methods=["GET","PUT","DELETE"])
# def handle_one_task(task_id):