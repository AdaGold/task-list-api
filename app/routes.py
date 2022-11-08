from crypt import methods
from flask import Blueprint,jsonify,make_response,request,abort
from app.models.task import Task 
from app import db

tasks_bp = Blueprint('tasks_bp',__name__, url_prefix='/tasks')

@tasks_bp.route('',methods = ['GET'])
def get_all_tasks():
    all_tasks = Task.query.all()
    result = []

    for task in all_tasks:
        result.append(task.to_dict())
    return jsonify(result), 200