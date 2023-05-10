from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)

    def is_complete(self):

        is_complete = None
        if self.completed_at is None:
            is_complete = False
        else:
            is_complete = True
        return is_complete


    @classmethod
    def dict_for_post_method(cls, tasks_details):

        result = cls(
            title=tasks_details["title"],
            description=tasks_details["description"],
            completed_at=None)
            # goal_id=tasks_details["goal_id"])
        return result
    

    def to_dict(self):
        return \
            {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": self.is_complete()
            }
    
    def to_dict_with_goal_id(self):
        return \
            {
                "id": self.task_id,
                "goal_id": self.goal_id,
                "title": self.title,
                "description": self.description,
                "is_complete": self.is_complete()
            }
