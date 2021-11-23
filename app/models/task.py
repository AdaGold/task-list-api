from flask import current_app, request
from app import db
from dotenv import load_dotenv
from sqlalchemy import desc,asc


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'))

    def task_dict(self):
        return {
            "id": self.task_id,
           # "goal_id": self.goal_id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at is not None
        }
    
