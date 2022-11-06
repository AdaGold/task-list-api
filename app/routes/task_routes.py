from app import db
from app.models.task import Task
from flask import Blueprint, request, make_response, jsonify

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

# CREATE ONE TASK w/ POST REQUEST
@tasks_bp.route("", methods=['POST'])
def create_task():
    # get post request data and convert to json
    request_body = request.get_json()

    # make a new instance of Task using request data
    new_task = Task(
        title=request_body["title"],
        description=request_body["description"]
        )

    # add new Task to database 
    db.session.add(new_task)
    db.session.commit()

    # return new task in json and successfully created status code
    return make_response(jsonify({"task": 
                    {"id": new_task.task_id,
                    "title": new_task.title,
                    "description": new_task.description,
                    "is_complete": new_task.is_complete
                    }}), 201)