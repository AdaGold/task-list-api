from flask import current_app
from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable = False)
    description = db.Column(db.String(300))
    completed_at = db.Column(db.DateTime)
