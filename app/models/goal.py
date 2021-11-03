from flask import current_app
from sqlalchemy.orm import backref
from app import db
from .task import Task


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True) 
    tasks=db.relationship('Task', backref='goal', lazy=True)
