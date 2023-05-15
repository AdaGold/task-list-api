from app import db
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint, jsonify, abort, make_response, request
from sqlalchemy import Column, Integer, String
# from sqlalchemy.orm import DeclarativeBase, mapped_column
# from sqlalchemy.ext.declarative import declarative_base

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
        description=task_data["description"]
        )
        
        return new_task

    def to_dict(self):
        return {
                'id': self.id,
                'title': self.title,
                'description': self.description,
                'is_complete': bool(self.completed_at)
            }
        
# # `/tasks?sort=asc`
# # @task_bp.route("/<task_id>", methods=["GET"])
#     def asc(self):
#         pass
#     # someselect.order_by(asc(table1.mycol))

#     # `/tasks?sort=desc
#     def desc(task_id):
#         pass
        
#     # someselect.order_by(desc(table1.mycol))