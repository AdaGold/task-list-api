from app import db
from app.models.goal import Goal
from flask import Blueprint, request, make_response, jsonify, abort
import datetime
from app.routes.route_helpers import validate_model


goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

#Create valid goal - post
@goals_bp.route("", methods=['POST'])

#need to add 404 for goals not found
def create_goal(cleient):
    request_body = request.get_json()
    new_goal = Goal(title=request_body['title'], id=request_body["id"])
    

    db.session.add(new_goal)
    db.session.commit()

    return make_response(jsonify({f"goal": new_goal}, 201))


#Getting all saved goals - get
@goals_bp.route("", methods=['GET'])
def get_all_goals():
    pass    


    
#Get goals when there are no saved goals - get

#Get one goal - get
@goals_bp.route("/<goal_id>", methods=['GET'])
def get_one_goal(goal_id):

    goal = validate_model(Goal, goal_id)
#use goal.to_dict()
    return { "id": goal.id,
        "title": goal.title,
         }


#Update a goal - put
@goals_bp.route("/<goal_id>", methods=['PUT'])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return make_response(jsonify({f"goal": goal.title}, 201))

#Delete a goal - delete
@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_book(goal_id):
   goal = validate_model(Goal, goal_id)

   db.session.delete(goal)
   db.session.commit()
   
   return make_response(jsonify({f"details": goal.id/goal.title/"successfully deleted"}, 201))

#No matching goal for get, update, or delete. Return 404 error.

#Create a goal with invalid title - post. Return 400 bad request.