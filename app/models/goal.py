from app import db
from app.models.task import Task


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship('Task', backref='goal')


    @classmethod
    def dict_for_post_method(cls, goal_details):

        result = cls(
            title=goal_details["title"])
        return result

    def to_dict(self):
        return \
            {
                "id": self.goal_id,
                "title": self.title,
            }
    

    # METHOD FOR PRINTING
    def tasks_dict(self):
        
        list_tasks = []
        for task in self.tasks:
            dict_tasks = {
                "id": task.task_id,
                "goal_id": task.goal_id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.is_complete()
            }
            list_tasks.append(dict_tasks)

        return list_tasks