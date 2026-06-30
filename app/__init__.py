from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    
    login_manager.init_app(app)
    login_manager.login_view = 'auth_routes.login'
    

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        # Use session.get for SQLAlchemy 2.0+ compatibility
        return db.session.get(User, int(user_id))

    # Register blueprints
    from app.core.resource_routes import resource_bp
    from app.core.history_routes import history_bp
    from app.core.points_routes import points_bp
    from app.frontend import frontend_bp
    from app.core.auth_routes import auth_bp
    from app.core.admin_routes import admin_bp
    from app.core.profile_routes import profile_bp
    from app.core.search_routes import search_bp
    from app.core.request_routes import request_bp
    
    app.register_blueprint(resource_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(points_bp)
    app.register_blueprint(frontend_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(request_bp)

    return app
