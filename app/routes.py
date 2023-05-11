from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task
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
    request_body = request.get_json()
    
    new_task = Task.from_dict(request_body)
    
    db.session.add(new_task)
    db.session.commit()
    
    return jsonify(f"New task: {new_task.title} successfully created!"), 201

## READ
@task_bp.route("", methods=["GET"])
def read_all_tasks():
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

## READ
@task_bp.route("/<task_id>", methods=["GET"])
def read_one_tasks(task_id):
    task = validate_model(Task, task_id)
    
    return task.to_dict(), 200

## UPDATE
@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()
    
    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body["completed_at"]

    db.session.commit()
    
    return task.to_dict(), 200

## DELETE
@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)
    
    db.session.delete(task)
    db.session.commit()
    
    return make_response(f"Task #{task.id} successfully deleted")

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
# # @task_bp.route('/tasks', methods=['GET', 'POST'])
# # def tasks():
# #     if request.method == 'GET':
# #         tasks = Task.query.all()
# #         return jsonify([task.to_dict() for task in tasks]), 200

# #     elif request.method == 'POST':
# #         request_data = request.get_json()

# #         title = request_data.get('title')
# #         description = request_data.get('description')

# #         task = Task(title=title, description=description)
# #         db.session.add(task)
# #         db.session.commit()

# #         return jsonify({'task': task.to_dict()}), 201

# # @task_bp.route('/tasks/<int:task_id>', methods=['GET', 'PUT', 'DELETE'])
# # def task(task_id):
# #     task = Task.query.get_or_404(task_id)

# #     if request.method == 'GET':
# #         return jsonify({'task': task.to_dict()}), 200

# #     elif request.method == 'PUT':
# #         request_data = request.get_json()

# #         title = request_data.get('title')
# #         description = request_data.get('description')

# #         task.title = title
# #         task.description = description
# #         db.session.commit()

# #         return jsonify({'task': task.to_dict()}), 200

# #     elif request.method == 'DELETE':
# #         db.session.delete(task)
# #         db.session.commit()

# #         return jsonify({}), 204

