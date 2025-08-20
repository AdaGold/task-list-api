from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from datetime import datetime
from typing import Optional
from sqlalchemy import ForeignKey


class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]]
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")

    def to_dict(self):
        if self.completed_at:
            completed = True
        else:
            completed = False

        task_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": completed,
        }

        if self.goal_id:
            task_dict["goal_id"] = self.goal_id

        return task_dict
    
    @classmethod
    def from_dict(cls, task_data):
        completed_at = task_data.get("completed_at")
        goal_id = task_data.get("goal_id")

        new_task = cls(
            title=task_data["title"],
            description=task_data["description"],
            completed_at=completed_at,
            goal_id=goal_id
        )

        return new_task