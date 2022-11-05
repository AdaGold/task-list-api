from flask import Blueprint

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")