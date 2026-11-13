
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..db import db


class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[datetime | None]

    goal_id: Mapped[int | None] = mapped_column(
        ForeignKey("goal.id")
    )

    goal = relationship("Goal", back_populates="tasks")

    def to_dict(self, include_goal=False):
        task_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at is not None
        }

        if include_goal:
            task_dict["goal_id"] = self.goal_id

        return task_dict

    @classmethod
    def from_dict(cls, task_data):
        return cls(
            title=task_data["title"],
            description=task_data["description"],
            completed_at=task_data.get("completed_at")
        )
