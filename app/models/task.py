from app import db
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import Column, Integer, String
# from sqlalchemy.ext.declarative import declarative_base
# from user import User, Base

# db = SQLAlchemy()

class Task(db.Model):

    # __tablename__ = "tasks"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)

    @classmethod
    def from_dict(cls, task_data):
        new_task = Task(
            title=task_data["title"],
            description=task_data["description"],
            completed_at=task_data["completed_at"]
        )

        return new_task

    def to_dict(self):
        return {
            'id': self.task_id,
            'title': self.title,
            'description': self.description,
            'is_complete': bool(self.completed_at)
        }