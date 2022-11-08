from app import db


class Task(db.Model):
    description = db.Column(db.String)
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    completed_at = db.Column(db.DateTime)
    title = db.Column(db.String)