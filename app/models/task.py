from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(length=40), nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    is_complete = db.Column(db.Boolean, default=False)

    @classmethod
    def from_dict(cls, task_data):
        return Task(
            title = task_data["title"],
            description = task_data["description"],
            completed_at = task_data["completed_at"]
        )
    
    def to_dict(self):
        return dict(
            task_id = self.task_id,
            title = self.title,
            description = self.description,
            is_complete = self.is_complete
        )