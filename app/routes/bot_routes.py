from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
from .routes_helper import error_message
from datetime import datetime

bot_token = "xoxb-3517483621795-3514864472709-eftmGUbZpBrItU54XIpAnwQo"

bot_bp = Blueprint("bot_bp", __name__, url_prefix="/")