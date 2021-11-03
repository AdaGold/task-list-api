from flask import Blueprint

# from .tasks import *
# from .goals import *

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")