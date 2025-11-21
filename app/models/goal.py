from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from sqlalchemy import String



class Goal(db.Model):

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    tasks: Mapped[list["Task"]] = relationship(
        back_populates="goal")

    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title
        }

    @classmethod
    def from_dict(cls, data_dict):
        if "title" not in data_dict:
            raise KeyError("title")
        return cls(title=data_dict["title"])