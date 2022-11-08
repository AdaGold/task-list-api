from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)


    @classmethod
    def from_dict(cls, goal_data):
        return cls(title=goal_data["title"])

    def to_dict(self):
        return dict(
            id=self.goal_id,
            title=self.title
        )

