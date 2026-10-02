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

def run_auto_migrations(app):
    """Automatically ensure database tables have all necessary columns on startup."""
    with app.app_context():
        try:
            from sqlalchemy import inspect, text
            insp = inspect(db.engine)
            existing_tables = insp.get_table_names()
            
            # Auto-create tables if completely missing
            if not existing_tables:
                db.create_all()
                existing_tables = insp.get_table_names()

            # Check users table
            if 'users' in existing_tables:
                user_cols = {c['name'] for c in insp.get_columns('users')}
                new_user_cols = [
                    ('last_login_ip', 'VARCHAR(45)'),
                    ('darpan_id', 'VARCHAR(50)'),
                    ('org_pan', 'VARCHAR(20)'),
                    ('pan_card_doc', 'VARCHAR(255)'),
                    ('auth_letter_doc', 'VARCHAR(255)'),
                    ('income_certificate_doc', 'VARCHAR(255)'),
                    ('income_verification_status', "VARCHAR(20) DEFAULT 'none'")
                ]
                with db.engine.begin() as conn:
                    for col_name, col_type in new_user_cols:
                        if col_name not in user_cols:
                            conn.execute(text(f"ALTER TABLE users ADD COLUMN {col_name} {col_type}"))
                            app.logger.info(f"Auto-migrated: added users.{col_name}")

            # Check resources table
            if 'resources' in existing_tables:
                res_cols = {c['name'] for c in insp.get_columns('resources')}
                if 'requires_income_proof' not in res_cols:
                    with db.engine.begin() as conn:
                        conn.execute(text("ALTER TABLE resources ADD COLUMN requires_income_proof BOOLEAN DEFAULT 0"))
                        app.logger.info("Auto-migrated: added resources.requires_income_proof")

            # Check ngo_likes table
            if 'ngo_likes' not in existing_tables:
                db.create_all()
                app.logger.info("Auto-migrated: created missing tables including ngo_likes")
        except Exception as e:
            app.logger.warning(f"Auto-migration check notice: {e}")


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

    # Run auto-migration check for deployment environments like PythonAnywhere
    run_auto_migrations(app)

    return app
