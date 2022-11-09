from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(length=40), nullable=False)
    tasks = db.relationship("Task", back_populates="goal")

    @classmethod
    def from_dict(cls, task_data):
        return Goal(
            title = task_data.get("title")
        )

    def to_dict(self):
        return dict(
            id = self.goal_id,
            title = self.title,
        )