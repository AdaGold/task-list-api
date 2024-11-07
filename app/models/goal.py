from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import db

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    tasks: Mapped[list["Task"]] = relationship(back_populates="goal")

    def to_dict(self):
        goal_to_dict = {
            "id": self.id,
            "title": self.title
        }
        return goal_to_dict
    
    @classmethod
    def from_dict(cls, goal_data):
        goal_dict = cls(title=goal_data["title"])
        return goal_dict