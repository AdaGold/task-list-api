from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    goal_title = db.Column(db.String)

