from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, request

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["GET", "POST"])
def handle_tasks():
    if request.method == "GET":
        tasks = Task.query.all()
        tasks_response = []
        for task in tasks:
            tasks_response.append({
                "id" : task.id,
                "title" : task.title,
                "description" : task.description,
                "completed_at" : task.completed_at
            })
        return jsonify(tasks_response)



    # elif request.method == "POST":
    #     request_body = request.get_json()
    #     new_task = Task(title=request_body["title"], 
    #     description=request_body["description"], completed_at=request_body["completed_at"])

    #     db.session.add(new_task)
    #     db.session.commit()

    #     return jsonify()
#GET /tasks
    #no saved tasks
    #one saved task

#POST /tasks
    #create a task where completed @ == None
    #ERROR: task with missing 'title' field
    #ERROR: task with missing 'description' field
    #create a task must contain completed @ (?????)

#GET /tasks/1
    #get existing taks
    #get a non-exisiting task

#PUT /tasks/1
    #update task 
    #update task not found

#DELETE /tasks/1
    #delete task
    #delete task not found



