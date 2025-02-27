from flask import Flask
from .routes.goal_routes import bp as goal_routes
from .routes.task_routes import bp as task_routes
from .db import db, migrate
from .models import task, goal
import os

def create_app(config=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    if config:
        # Merge `config` into the app's configuration
        # to override the app's default settings for testing
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    app.register_blueprint(task_routes)
    app.register_blueprint(goal_routes)

    return app
