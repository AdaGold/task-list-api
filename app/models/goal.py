from app import db


class Goal(db.Model):
   goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   title = db.Column(db.String)

   #holds a list of Task instances connected to the Goal
   #Does not just have the id, has the whole instance
   tasks = db.relationship("Task", backref="goal", lazy = True)
   #goal.tasks becomes a list of the tasts

   #post is different, if i make a Goal and add Tasks,
   #I need to look those tasks up and add them to the goal