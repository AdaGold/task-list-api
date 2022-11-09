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
        #new_goal = Goal.from_dict(request_body)

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



@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_task(goal_id):
    request_body = request.get_json()

    goal = validate_model(Goal, goal_id)
    
    goal_tasks_data = []

    # loop through the request body and grab each task_id
    for task_id in request_body["task_ids"]:

        # create instance of each task 
        new_task = validate_model(Task, task_id)

        # assign each task to goal
        new_task.goal = goal

        # add all the task ids to goal_tasks_data list
        goal_tasks_data.append(new_task.task_id)
    
    db.session.add(new_task)
    db.session.commit()
    #new_task = Task.from_dict(request_body)
    # goal_tasks = Goal(
    #     tasks=request_body["task_ids"]
    # )

    #goal_id should be the key, with a list of task

    return {"id": goal.goal_id, "task_ids": goal_tasks_data}



#needs to work for specifical goal with no tasks and get tasks for specific goal with tasks
@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_all_tasks(goal_id):

  
    goal = validate_model(Goal, goal_id)

    if not goal:
        return ""

    #need to print out goal id and info with task.to_dict
    tasks_response = []
    for task in goal.tasks:
        tasks_response.append(task.to_dict())

    response_body = goal.to_dict()
    response_body["tasks"] = tasks_response
    return response_body


    