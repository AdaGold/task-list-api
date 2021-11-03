from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import request, jsonify
from routes import goals_bp


@goals_bp.route("", methods=["GET", "POST"])
def goals():
    if request.method == "GET":
        goals = Goal.query.all()
        response_body = [goal.to_dict() for goal in goals]
        return jsonify(response_body), 200

    elif request.method == "POST":
        request_body = request.get_json()

        if "title" not in request_body:
            return jsonify({"details": "Invalid data"}), 400

        new_goal = Goal.from_dict(request_body)

        db.session.add(new_goal)
        db.session.commit()

        response_body = {
            "goal": new_goal.to_dict()
        }

        return jsonify(response_body), 201

@goals_bp.route("/<id>", methods=["GET", "PUT", "DELETE"])
def goal_id(id):
    goal = Goal.query.get(id)

    if not goal:
        return jsonify(None), 404

    if request.method == "GET":
        response_body = {
            "goal": goal.to_dict()
        }
        return jsonify(response_body), 200

    elif request.method == "PUT":
        request_body = request.get_json()
        goal.title = request_body["title"]

        db.session.commit()

        response_body = {
            "goal": goal.to_dict()
        }

        return jsonify(response_body), 200

    elif request.method == "DELETE":
        db.session.delete(goal)
        db.session.commit()

        response_body = {
            "details": f"Goal {id} \"{goal.title}\" successfully deleted"
        }

        return jsonify(response_body), 200

@goals_bp.route("/<id>/tasks", methods=["GET", "POST"])
def goal_id_tasks(id):
    goal = Goal.query.get(id)

    if not goal:
        return jsonify(None), 404

    if request.method == "GET":
        return goal.to_dict(tasks=True), 200

    elif request.method == "POST":
        try:
            task_ids = request.get_json()["task_ids"]
        except KeyError:
            return jsonify("test"), 400

        for task_id in task_ids:
            task = Task.query.get(task_id)
            task.goal = goal

        db.session.commit()

        response_body = {
            "id": goal.id,
            "task_ids": task_ids
        }

        return jsonify(response_body), 200
