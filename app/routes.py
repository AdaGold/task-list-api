from flask import Blueprint, jsonify
from app.models.task import Task
from app import db

task_bp = Blueprint("task", __name__, url_prefix="/task")


