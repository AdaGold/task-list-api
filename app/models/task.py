from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy import ForeignKey
from ..db import db
from sqlalchemy import String, Date
from datetime import datetime
from flask import Blueprint, abort, make_response, request, Response
from typing import Optional
from datetime import date

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255))
    completed_at:Mapped[date] = mapped_column(Date, nullable=True)

    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")

    def to_dict(self): # json
        
        
        task_dict = {"id": self.id,
                "title":self.title,
                "description":self.description,
                "is_complete": self.completed_at is not None}
        
        if self.goal_id is not None:
            task_dict["goal_id"] = self.goal_id
            
        
        return task_dict
        
    @classmethod
    def from_dict(cls, data_dict):
        if "title" not in data_dict:
           
            raise KeyError("title")
        if "description" not in data_dict:
            raise KeyError("description")
        
        return cls(
            title=data_dict["title"],
            description=data_dict["description"],
            completed_at=None  # default to None when creating
        )
        
    
    