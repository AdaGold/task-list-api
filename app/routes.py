from flask import Blueprint, request, make_response, jsonify
#To access incoming request data, you can use the global request object. 
#Response is a Flask class that represents HTTP responses.
    #but we use a helper method, make_response?
from app import db
from app.models.task import Task
from datetime import datetime
#from app.models.goal import Goal

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
#Our Blueprint instance. We'll use it to group routes that start with /tasks. 
    # "tasks" is the debugging?? name for this Blueprint. 
    #__name__ provides information the blueprint uses for certain aspects of routing.?

@tasks_bp.route("", methods=["POST","GET"])
#I still don't really get how decorators work
#but anyway this one is for if you want to generally post 
#or if you want to get all tasks
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
            #db.session is the database's way of collecting changes that need to be made. 
            #Here, we are saying we want the database to add new_task, and then save and commit

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
#this is for when there's a specific task
def handle_a_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response('',404)

    elif request.method == "GET":
        return {"task": { "id": task.task_id,
                        "title": task.title,
                        "description": task.description,
                        "is_complete": False if task.completed_at is None else task.completed_at  
                        }}
                        
    elif request.method == "PUT":
        form_data = request.get_json()

        task.title = form_data["title"]
        task.description = form_data["description"]
        #task.completed_at = form_data["completed_at"]

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
        print(task)
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