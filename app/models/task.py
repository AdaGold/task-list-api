from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(length=40), nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, default=None)
    is_complete = db.Column(db.Boolean, default=False)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'))
    goal = db.relationship("Goal", back_populates="tasks")

    @classmethod
    def from_dict(cls, task_data):
        return Task(
            title = task_data.get("title"),
            description = task_data.get("description"),
            completed_at = task_data.get("completed_at", None)
        )

    def to_dict(self):
        if not self.goal_id:
            return dict(
                id = self.id,
                title = self.title,
                description = self.description,
                is_complete = self.is_complete
            )

        return dict(
            id = self.id,
            goal_id = self.goal_id,
            title = self.title,
            description = self.description,
            is_complete = self.is_complete
        )