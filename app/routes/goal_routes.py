from app import db
from app.models.goal import Goal
from flask import Blueprint, request, make_response, jsonify, abort
from app.routes.route_helpers import validate_model

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

#validate goal as integer
def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except: 
        abort(make_response({"message": f"{goal_id} is invalid"}, 400))

    goal = Goal.query.get(goal_id)

    if not goal:
        abort(make_response({"message": f"{goal_id} is invalid"}, 404))

    return goal

#create a goal 

@goals_bp.route("", methods=['POST'])
def create_goal():
   request_body = request.get_json()

   if not "title" in request_body:
        return jsonify({"details": "Invalid data"}), 400

   new_goal = Goal(title = request_body["title"])

   db.session.add(new_goal)
   db.session.commit()

   return {
    "goal": new_goal.to_dict()
   }, 201


# Get one goal 
@goals_bp.route("/<goal_id>", methods=['GET'])
def get_one_goal(goal_id):
    #call helper function to validate the task_id
    goal = validate_goal(goal_id)
    
    # return dictionary with Task data for one task
    return {"goal": goal.to_dict()}


#need to finish test
#Update a goal - put
@goals_bp.route("/<goal_id>", methods=['PUT'])
def update_goal(goal_id):
    goal = validate_goal(goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.add(goal)
    db.session.commit()

    return make_response(jsonify({f"goal": goal.title}, 201))

@goals_bp.route("", methods = ["GET"])
def get_goals():
    goals = Goal.query.all()
    goals_json = [] 

    for goal in goals:
        goals_json.append(goal.to_dict())

    return jsonify(goals_json)




#Delete a goal - delete
@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
   goal = validate_goal(goal_id)

   db.session.delete(goal)
   db.session.commit()
   
   return make_response({"details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"})
