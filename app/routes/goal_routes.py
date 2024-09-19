from flask import Blueprint
from ..db import db

bp = Blueprint("goals_bp", __name__, url_prefix="/goals")