from flask import Flask
from flask_login import current_user
from app.config import Config
from app import api, user
from app.extensions import db, migrate, login_manager
from app.user.models import User

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    blueprint_register(app)
    extension_register(app)

    return app

def blueprint_register(app: Flask):
    app.register_blueprint(api.views.blueprint)
    app.register_blueprint(user.views.blueprint)

def extension_register(app: Flask):
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager_register(app)

def login_manager_register(app: Flask):
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.context_processor
    def inject_data():
        return dict(user=current_user)
