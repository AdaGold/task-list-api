from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship("Task", back_populates="goal")

    @classmethod
    def from_dict(cls, goal_data):
        return Goal(title=goal_data["title"])

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title
        }
