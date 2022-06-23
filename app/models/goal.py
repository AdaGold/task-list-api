from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)

    def to_dict(self):
        tasks_info = [task.to_dict() for task in self.tasks]

        goal_dict = dict(
            id = self.id,
            title = self.title,
            tasks = tasks_info
        )
        return goal_dict

    @classmethod
    def from_dict(cls, data_dict):
        return cls(
            title = data_dict["title"]
        )