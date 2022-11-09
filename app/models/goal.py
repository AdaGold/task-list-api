from app import db

# One Side
class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    tasks = db.relationship('Task', back_populates="goal")

    def to_dict(self):
        result = {
            "id": self.goal_id,
            "title": self.title
            }

        return result
    

    # def get_tasks_list(self):
    #     list_of_tasks = []
    #     for item in self.task_items:
    #         list_of_tasks.append(item.to_dict())
    #     return list_of_tasks
    
    @classmethod
    def from_dict(cls, task_dict):
        return cls(
            title=task_dict["title"]
        )