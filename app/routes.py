from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task
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
    
    if not request_body.get('title') or not request_body.get('description'):
        abort(make_response({"details": "Invalid data"}, 400))
        
    task = Task.from_dict(request_body)
    
    db.session.add(task)
    db.session.commit()
    return {"task": task.to_dict()}, 201

## READ - ALL
@task_bp.route("", methods=["GET"])
def get_all_tasks():
    task_query = request.args.get("sort")
    if task_query == 'asc':
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif task_query == 'desc':
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()

    tasks_response = []
    
    for task in tasks:
        task_dict = task.to_dict()
        tasks_response.append(task_dict)
    
    return jsonify(tasks_response), 200

## READ - ONE
@task_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id)

    return {"task": task.to_dict()}, 200


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
# # define a route for creating a task resource
# def create_goal():
#     request_body = request.get_json()
    
#     new_goal = Goal(
#         title=request_body["title"]
#     )
    
#     db.session.add(new_goal)
#     db.session.commit()
    
#     return jsonify(f"New goal: {new_goal.title} successfully created!"), 201

# @goal_bp.route("", methods=["GET"])
# def read_all_goals():
    
#     goals = Goal.query.all()
        
#     goals_response = []
    
#     for goal in goals:
#         goals_response.append({ "name": goal.name, "id": goal.id })
    
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
