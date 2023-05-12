from os import abort
from app import db
from app.models.goal import Goal
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
from datetime import datetime
import requests
import os
from dotenv import load_dotenv
load_dotenv()
