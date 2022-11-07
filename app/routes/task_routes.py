from app import db
from app.models.task import Task
from flask import Blueprint, request, make_response, jsonify, abort
from sqlalchemy import asc, desc
import datetime

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

# CREATE ONE TASK w/ POST REQUEST
@tasks_bp.route("", methods=['POST'])
def create_task():
    # use try / except to catch KeyError for invalid data
    try:
        # get post request data and convert to json
        request_body = request.get_json()

        # make a new instance of Task using request data
        new_task = Task.from_dict(request_body)

        # add new task to database 
        db.session.add(new_task)
        db.session.commit()

        # return new task in json and successfully created status code
        return make_response(jsonify({f"task": new_task.to_dict()}), 201)
    
    except KeyError:
        # abort and show error message if KeyError
        abort(make_response({"details": "Invalid data"}, 400))

# GET ALL TASKS w/ GET REQUEST
@tasks_bp.route("", methods=['GET'])
def get_all_tasks():
    
    #variable to store the tasks in 
    sort_tasks = request.args.get("sort")

    #order tasks titles in ascending or descending order depending on sort type, if neither return all 
    if sort_tasks == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort_tasks == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()

    tasks_response = []

    # loop through all the instances of Task, add to response body
    # convert Task data into dictionary
    for task in tasks:
        tasks_response.append(task.to_dict())
    
    # convert response into json and give successful status code
    return jsonify(tasks_response), 200


#VALIDATE TASK ID, IF TASK_ID NOT FOUND OR INVALID RETURN 404
def validate_task(task_id):
    #this code can be refactored to handle invalid data
    # try:
    #     task_id = int(task_id)
    # except:
    #     abort(make_response({"message":f"{task_id} is invalid"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message": f"{task_id} not found"}, 404))
    return task 


# GET ONE TASK w/ GET REQUEST
@tasks_bp.route("/<task_id>", methods=['GET'])
def get_one_task(task_id):
    #call helper function to validate the task_id
    task = validate_task(task_id)
    

    # return dictionary with Task data for one task
    return {"task": task.to_dict()}


# UPDATE ONE TASK w/ PUT REQUEST
@tasks_bp.route("/<task_id>", methods=['PUT'])
def update_task(task_id):
    #call helper function to validate the task_id
    task = validate_task(task_id)

    # get put request data and convert to json
    request_body = request.get_json()

    # update task attributes according to request data
    task.title = request_body["title"]
    task.description = request_body["description"]

    # update task in the database
    db.session.commit()

    # return updated task as a dictionary
    return {"task": task.to_dict()}


# DELETE ONE TASK w/ DELETE REQUEST
@tasks_bp.route("/<task_id>", methods=['DELETE'])
def delete_task(task_id):
    #call helper function to validate the task_id
    task = validate_task(task_id)

    # delete task from the database
    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f"Task {task.task_id} \"{task.title}\" successfully deleted"})

# MARK COMPLETE w/ PATCH REQUEST
@tasks_bp.route("/<task_id>/mark_complete", methods=['PATCH'])
def mark_complete_task(task_id):
    # call helper to validate task 
    task = validate_task(task_id)
    
    # update completed_at from None to current date
    task.is_complete = True
    task.completed_at = datetime.date.today()

    # update task in the database
    db.session.commit()

    return {"task": task.to_dict()}

# MARK INCOMPLETE w/ PATCH REQUEST
@tasks_bp.route("/<task_id>/mark_incomplete", methods=['PATCH'])
def mark_incomplete_task(task_id):
    # call helper to validate task 
    task = validate_task(task_id)
    
    # update completed_at from current date to None
    task.is_complete = False
    task.completed_at = None

    # update task in the database
    db.session.commit()

    return {"task": task.to_dict()}