from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, Request

# Instantiate Blueprint instances here
tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")
