from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.core import resource_bp, history_bp, points_bp
    from app.frontend import frontend_bp
    
    app.register_blueprint(resource_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(points_bp)
    app.register_blueprint(frontend_bp)

    return app
