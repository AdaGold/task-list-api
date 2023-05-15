from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task
    # review then evaluate if needed:
from sqlalchemy import asc
    # vscode asc breadcrum notes:
# statement symbol()
# statement _create_asc(column)
# asc = public_factory(UnaryExpression._create_asc, ".sql.expression.asc")
# Full name: sqlalchemy.sql.expression.asc
    # review then evaluate if needed:
from sqlalchemy import desc
    # review then evaluate if needed:
from datetime import datetime
    # review then evaluate if needed:
# from flask import Flask
    # uncomment when implementing goal model:
# from app.models.goal import Goal

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
    # uncomment when implementing goal model:
# goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{model_id} is not a valid type ({type(model_id)}). Must be an integer)"}, 400))

    model = cls.query.get(model_id)
    
    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} does not exist"}, 404))
        
    return model
        
## CREATE
@task_bp.route("", methods=['POST'])
def create_task():
# def create_task(task_title, task_description):
    # task = validate_model(Task)
    
    request_body = request.get_json()
    
    if not request_body.get('title') or not request_body.get('description'):
        abort(make_response({"details": "Invalid data"}, 400))
        
    task = Task.from_dict(request_body)
    
    db.session.add(task)
    db.session.commit()
 
    return {"task": task.to_dict()}, 201

## READ 
@task_bp.route("", methods=["GET"])
def get_all_tasks():
    title_query = request.args.get("title")
    description_query = request.args.get("description")
    
    if title_query:
        tasks = Task.query.filter_by(title=title_query)
    elif description_query:
        tasks = Task.query.filter_by(description=description_query)
    else:
        tasks = Task.query.all()
        
    tasks_response = []
    
    for task in tasks:
        tasks_response.append(task.to_dict())
    
    return jsonify(tasks_response)

# READ
@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    
    return {"task": task.to_dict()}, 200
    
# READ - SORTED 
# # ASCENDING TITLE READ_ALL_TASKS
    # SUDO CODE:
# # @task_bp.route("", methods=["GET"])
# # def read_all_tasks():
#     # asc_title = request.args.get("sort")
    
#     # get all tasks
#     # 
#     # if sort == "asc" use sorted method (of dict title value)
#     # elif sort for desc
#     # or sort == "desc"

@task_bp.route("", methods=["GET"])
# def get_tasks_sorted():
#     sort_order = requests.args.get("sort")
    
#     if sort_order == "asc":
#         sorted_tasks = sorted(tasks.items(), key=lambda x: x[1]["title"])
#         tasks = list(sorted_tasks)    
#     elif sort_order == "desc":
#         sorted_tasks = sorted(tasks.items(), key=lambda x: x[1]["title"], reverse=True)
#         tasks = list(sorted_tasks)
        
#     return tasks
@task_bp.route("", methods=["GET"])
def get_sorted_tasks():
    
    sort_order = request.args.get("sort")
    
    if sort_order == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort_order == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()
        
    ordered_tasks = []

    for task in tasks:
        ordered_tasks.append(task.to_dict())
    
    return jsonify(ordered_tasks), 200
    

## UPDATE
@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()
    
    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()
        
    return {"task": task.to_dict()}, 200

## DELETE
@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)
    
    db.session.delete(task)
    db.session.commit()
    
    return {
        "details": f'Task {task_id} "{task.title}" successfully deleted'
    }


###############################
    # review and evaluation implementing after task routes are passing tests:
    # (code below references learn lessons and flasky live code for healer routes)
#### Goal Routes:
# @goal_bp.route("", methods=['POST'])
# # define a route for creating a crystal resource
# def create_goal():
#     request_body = request.get_json()
    
#     new_goal = Goal(
#         title=request_body["title"]
#     )
    
#     db.session.add(new_goal)
#     db.session.commit()
    
#     return jsonify(f"New goal: {new_goal.title} successfully created!"), 201

# @goal_bp.route("", methods=["GET"])
# def read_all_healers():
    
#     healers = Healer.query.all()
        
#     healers_response = []
    
#     for healer in healers:
#         healers_response.append({ "name": healer.name, "id": healer.id })
    
#     return jsonify(healers_response)

# @goal_bp.route("/<goal_id>/tasks", methods=["POST"])
# def create_task_by_id(goal_id):

#     goal = validate_model(Goal, goal_id)

#     request_body = request.get_json()

#     new_task = Task(
#         title=request_body["title"],
#         description=request_body["description"],
#         completed_at=request_body["completed_at"],
#         goal=goal
#     )

#     db.session.add(new_task)
#     db.session.commit()

#     return jsonify(f"Task {new_task.title} owned by {new_task.goal.title} was successfully created."), 201

# @goal_bp.route("/<goal_id>/tasks", methods=["GET"])
# def get_all_tasks_with_id(goal_id):
#     goal = validate_model(Goal, goal_id)

#     task_response = []

#     for goal in goal.tasks:
#         goal_response.append(task.to_dict())

#     return jsonify(goal_response), 200

# @goal_bp.route("/<goal_id>", methods=["GET"])
# def get_goal_by_id(goal_id):
#     goal = validate_model(Goal, goal_id)

#     return jsonify({
#         "id": goal.id,
#         "title": goal.name
#     }), 200


# ###########################################
# #### Early Implimentation of Task Routes:
#     # review then decide how or if to impliment:
# @task_bp.route('/tasks', methods=['GET', 'POST'])
# def tasks():
#     if request.method == 'GET':
#         tasks = Task.query.all()
#         return jsonify([task.to_dict() for task in tasks]), 200

#     elif request.method == 'POST':
#         request_data = request.get_json()

#         title = request_data.get('title')
#         description = request_data.get('description')

#         task = Task(title=title, description=description)
#         db.session.add(task)
#         db.session.commit()

#         return jsonify({'task': task.to_dict()}), 201

# @task_bp.route('/tasks/<int:task_id>', methods=['GET', 'PUT', 'DELETE'])
# def task(task_id):
#     task = Task.query.get_or_404(task_id)

#     if request.method == 'GET':
#         return jsonify({'task': task.to_dict()}), 200

#     elif request.method == 'PUT':
#         request_data = request.get_json()

#         title = request_data.get('title')
#         description = request_data.get('description')

#         task.title = title
#         task.description = description
#         db.session.commit()

#         return jsonify({'task': task.to_dict()}), 200

#     elif request.method == 'DELETE':
#         db.session.delete(task)
#         db.session.commit()

#         return jsonify({}), 204

