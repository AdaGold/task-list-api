from app.models.task import Task
from flask import Blueprint, jsonify, request
from app import db
from app.routes_helper import validated_task

# tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# @tasks_bp.route("", methods=["GET"])
# def get_s():
#     task_query = request.args

#     if "sort" in task_query:
#         if task_query["sort"] == "desc":
#             tasks = Task.query.order_by(desc(Task.title)).all()
#         else:
#             tasks = Task.query.order_by(asc(Task.title)).all()
#     else:
#         # To get all the task from the table
#          tasks = Task.query.all()

#     tasks_response = [task.to_json() for task in tasks]

#     return jsonify(tasks_response)