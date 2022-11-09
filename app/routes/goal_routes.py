from app import db
from app.models.goal import Goal
from flask import Blueprint, request, make_response, jsonify, abort
from app.models.task import Task
from app.routes.route_helpers import validate_model

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

#Get all goals - GET 
@goals_bp.route("", methods = ["GET"])
def get_goals():

#get all of the goals 
    goals = Goal.query.all()
    goals_response = [] 

#loop through all goals, append to goals_response list, call helper function to create dict
    for goal in goals:
        goals_response.append(goal.to_dict())

    return jsonify(goals_response)

#Create a new goal - POST
#Refactor ? 
@goals_bp.route("", methods=['POST'])
def create_goal():

    try:
        request_body = request.get_json()
        new_goal = Goal(title = request_body["title"])

        db.session.add(new_goal)
        db.session.commit()

        return {
        "goal": new_goal.to_dict()
   }, 201

    except KeyError: 
        abort(make_response({"details": "Invalid data"}, 400))

#Get a goal - GET 
@goals_bp.route("/<goal_id>", methods=['GET'])
def get_one_goal(goal_id):

    #call helper function to validate the task_id
    goal = validate_model(Goal, goal_id)
    
    #return dictionary with goal data, call helper function
    return {"goal": goal.to_dict()}

#Update a goal - PUT
@goals_bp.route("/<goal_id>", methods=['PUT'])
def update_goal(goal_id):

    #validate goal using helper function
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.add(goal)
    db.session.commit()

    #return dictionary with goal data, call helper function
    return {"goal": goal.to_dict()}

#Delete a goal - delete
@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):

   #validate goal using helper function
   goal = validate_model(Goal, goal_id)

   db.session.delete(goal)
   db.session.commit()
   
   return make_response({"details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"})

# #validate goals
# #update to use validate models function
# def validate_goal(goal_id):
#     try:
#         goal_id = int(goal_id)
#     except: 
#         abort(make_response({"message": f"{goal_id} is invalid"}, 400))

#     goal = Goal.query.get(goal_id)

#     if not goal:
#         abort(make_response({"message": f"Goal {goal_id} not found"}, 404))

#     return goal




# @goals_bp.route("/<goal_id>/tasks", methods=["POST"])
# def create_task(goal_id):

#     goal = validate_model(Goal, goal_id)

#     request_body = request.get_json()

#     new_task = Task.from_dict(request_body)
#     new_task.goal = goal
    
#     db.session.add(new_task)
#     db.session.commit()

#     return make_response(jsonify(f"{goal.goal_id} {new_task.id} "))


#needs to work for specifical goal with no tasks and get tasks for specific goal with tasks
@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_all_tasks(goal_id):

  
    goal = validate_model(Goal, goal_id)

    tasks_response = []
    for task in goal.tasks:
        tasks_response.append(task.to_dict())
    return jsonify(tasks_response)


    #test response expected for no tasks
    #needs to return empty list when there is no tasks
    # assert response_body == {
    #     "id": 1,
    #     "title": "Build a habit of going outside daily",
    #     "tasks": []
    # }
